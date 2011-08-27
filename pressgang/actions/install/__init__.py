
from django.template.defaultfilters import slugify
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _

from pressgang.actions import Action
from pressgang.actions.install.exceptions import InstallationError
from pressgang.actions.install.models import InstallationRecord
from pressgang.actions.options import ActionWithOptions
from pressgang.core.exceptions import PressGangConfigurationError
from pressgang.core.models import Blog, WordPressVersion
import pressgang.settings as _settings

import datetime
import inspect
import os
import re

def find_installers():
	"""Finds a list of all available installers.

	The installers are returned in a tuple of tuples sorted by the display
	name of the installer, formatted as (module_path, display_name).

	Returns: a list of installer module paths and names

	"""
	installers = []
	for module_path in _settings.INSTALLERS:
		installer = load_installer(module_path)
		installers.append((module_path, installer.get_display_name()))
	return tuple(sorted(installers, key=lambda i: i[1]))

def load_installer(package_path):
	"""Loads an installer contained in the given Python package.

	Arguments:
	package_path -- a string of the installer package's possible path

	Returns: a class descended from Installer in the given package

	"""

	# Attempt to import the installer from the given package
	try:
		installer_package = import_module(package_path)
	except ImportError:
		raise PressGangConfigurationError(_("The installer package %(package)s does not appear to be valid.") % {'package': package_path})
	try:
		return installer_package.Install
	except AttributeError:
		raise PressGangConfigurationError(_("The installer package %(package)s does not appear to contain a valid %(class)s class.") % {'package': package_path, 'class': 'Install'})

class InstallAction(Action):
	"""Abstract base class defining how to install a WordPress blog."""

	__metaclass__ = ActionWithOptions

	# The version of WordPress that this installer installs
	wp_version = None

	# Whether or not this installer creates a multiple-blog version of WordPress
	multiple_blogs = False

	# The database host to use
	db_host = "localhost"

	# The default character set to use when creating the database
	db_charset = "utf8"

	# The default collation to use when creating the database
	db_collation = "utf8_general_ci"

	# The administrator's email address
	admin_email = None

	# The name to use for the administrator account
	admin_username = "admin"

	display_name = _("installation")

	Record = InstallationRecord

	log_template = "pressgang/install/record.html"
	execute_template = "pressgang/install/install.html"

	steps = [
		'pressgang.actions.install.steps.wpfiles',
		'pressgang.actions.install.steps.db',
		'pressgang.actions.install.steps.apache',
		'pressgang.actions.install.steps.configuration',
		'pressgang.actions.install.steps.wpcontent',
		'pressgang.actions.install.steps.customization'
	]

	# Since we're installing a blog, there is nothing to revert back to
	supports_reversion = False

	# A search for unsafe characters in a WordPress username
	_UNSAFE_USERNAME_CHARS = re.compile(r'[^a-zA-Z0-9]')

	def __init__(self, blog=None, slug=None, title=None, description=None, admins=[], users=[], password=None, is_public=False):
		"""Creates a new installer

		This can be passed an existing Blog instance, which will treat the installer
		more as a guide for how to configure additiona components of an already
		installed blog.  For example, adding child blogs to an already installed
		blog might make use of this installer to provide configuration settings,
		but would not actually require a blog to be installed

		Keyword Arguments:
		blog -- a Blog instance
		slug -- the URL slug for the blog
		title -- the full title of the blog
		description -- the full description of the blog
		admins -- a list of admin email addresses
		users -- a list of user email addresses
		password -- the password to use with the admin account
		is_public -- whether or not the blog is findable by crawlers

		"""

		# Make sure that the installer defines required values
		module_name = inspect.getmodule(self).__name__
		if not self.display_name:
			raise PressGangConfigurationError(_("The installer %(installer)s must define a display name by setting a value for display_name.") % {'installer': module_name})
		if not self.admin_email:
			raise PressGangConfigurationError(_("The installer %(installer)s must define an administrator email address by setting a value for admin_email.") % {'installer': module_name})
		if not self.wp_version:
			raise PressGangConfigurationError(_("The installer %(installer)s must define a version of WordPress to install by setting a value for wp_version.") % {'installer': module_name})

		# Get dummy install values from an existing blog
		if blog:
			self.slug = os.path.basename(blog.path)
			self.title = blog.title
			self.description = None
			self.admins = []
			self.users = []
			self.password = blog.admin_password
			self.is_public = True
			self.version = blog.version
			self.path = blog.path

		# Get actual installation values from the user's form data
		else:
			self.slug = slug
			self.title = title
			self.description = description
			self.admins = admins
			self.users = users
			self.password = password
			self.is_public = is_public

			# Determine internally used version and path information
			self.version = self._determine_version()
			self.path = self._determine_installer_path()

			# Remove any blogs in the database sharing this path that no longer
			# actually exist on the file system.  If there is a blog sharing
			# the path that exists, however, raise an error indicating this.
			install_path = self._get_installation_path()
			try:
				old_blog = Blog.objects.get(path=install_path)
			except Blog.DoesNotExist:
				pass
			else:
				if not old_blog.is_valid:
					old_blog.delete()
				else:
					raise InstallationError(_("The installation directory for this blog (%(dir)s) is not available.") % {'dir': install_path})

			# Create a new blog and pass it to the installer
			blog = Blog.objects.create(
				path = install_path,
				title = self.title,
				version = self.version,
				created = datetime.datetime.now(),
				admin_user = self.admin_username,
				admin_password = self.password,
				is_managed = True)

		# Move forward using either the existing blog or the new one
		super(InstallAction, self).__init__(blog)

	@classmethod
	def get_display_name(cls):
		"""Return the display name of the installer.

		If the child installer has set the `display_name` class variable, that
		value will be used.  If not, the name of the class will be used.

		Returns: the display name for the installer

		"""
		parts = [cls.display_name or cls.__name__]
		if cls.wp_version:
			parts.append("(%s)" % cls.wp_version)
		return " ".join(parts)

	@property
	def name(self):
		"""The installer's name."""
		return self.__class__.get_display_name()

	def provide_blog_dir(self):
		"""
		Allows a child installer to provide additional installation directory
		information.

		This should return a relative path, which will be be placed between the
		Apache document root and the URL slug given for the blog.

		Returns: a relative path used to determine the installation path

		"""
		return ""

	def provide_db_base_name(self):
		"""Provides the base name of the database to use.

		If overriden, a child installer does not need to worry about returning
		a unique name, as enforcement of uniqueness is handled elsewhere.

		By default, a database name is generated based on the version of
		WordPress being installed and the blog's slug.

		Returns: the base name of the database to use for the blog

		"""
		return "_".join([
			self._make_db_prefix_from_version(),
			self.slug])

	def provide_db_user_base_name(self):
		"""Provides the name of the blog's database user.

		If overriden, a child installer does not need to worry about returning
		a unique name, as enforcement of uniqueness is handled elsewhere.

		By default, a username is created based solely on the blog's slug.

		Returns: the base name of the database user for the blog

		"""
		return "_".join([
			self._make_db_prefix_from_version(),
			self.slug])

	def provide_username(self, email):
		"""Provide a username to use for the given email.

		This is used by the installer when adding new users.  By default, the
		username will be the safe slugified version of the non-domain part of the email.

		Arguments:
		email -- a new user's email address

		Returns: a valid WordPress username

		"""
		return re.sub(self._UNSAFE_USERNAME_CHARS, '', slugify(email.split("@")[0]))

	def provide_user_blog_slug(self, email):
		"""Provide the value of the slug for the blog to be created for the user.

		This is used by an installer installing a WPMU or multisite blog during
		the creation of blogs for any non-admin users.  By default, the blog
		slug will be the user's username.

		Arguments:
		email -- the email address of the user

		Returns: the blog slug for the user

		"""
		return self.provide_username(email)

	def provide_child_blog_title(self, email):
		"""Provide the title for a child blog for the user with the given email.

		This is used by an installer installing a WPMU or multisite blog during
		the creation of blogs for any non-admin users.  By default, the blog
		title will be "My Blog".

		Arguments:
		email -- the email address of the blog owner

		Returns: the title for the blog

		"""
		return _("My Blog")

	def on_error(self, blog, e):
		"""Delete the blog's database record if installation did not succeed."""
		blog.delete()

	def _get_installation_path(self):
		"""Get the full path to the installation directory.

		This is determined by combining Apache's DocumentRoot setting, any
		custom directory information provided by `provide_blog_dir`

		Returns: the full path to the installation directory

		"""
		return os.path.join(
			_settings.APACHE_DOCUMENT_ROOT,
			self.provide_blog_dir(),
			self.slug
		)

	def _make_db_prefix_from_version(self):
		"""Makes a prefix used in database names determined by the version.

		Returns: a database prefix corresponding to the WordPress version

		"""
		if self.version.is_multi:
			return "wpmu"
		else:
			return "wp"

	def _determine_version(self):
		"""Return a WordPressVersion instance for this installer's version.

		The version of WordPress that an installer installs is determined by
		the value of its `wp_version` member variable, which will simply be
		a string of the WordPress version to install.

		Returns: a WordPressVersion instance

		"""
		return WordPressVersion.objects.get_from_string(self.wp_version, is_multi=self.multiple_blogs)

	def _determine_installer_path(self):
		"""Determine the full path to the current installer.

		This is needed due to the fact that the optional theme and plugin
		directories reside in the same directory as the installer.

		Returns: the full path to the current installer.

		"""
		return os.path.dirname(inspect.getfile(self.__class__))
