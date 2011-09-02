
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.steps import InstallationStep
from pressgang.actions.install.exceptions import InstallationError
import pressgang.settings as _settings

import httplib
import os
import shutil
import tempfile
import urllib
import urllib2

class Step(InstallationStep):

	name = _("WordPress initial configuration")

	# Text used on a line that should be deleted in a .php file
	_DELETION_FLAG = "PRESSGANG_DELETE"

	def execute(self, blog, installer):
		"""Brings the blog to a state where it can be visited."""

		# Create a configuration file for the installation
		self.start(_("Creating WordPress configuration file."))
		try:
			config_file = open(blog.config_file_path, 'w')
		except OSError, e:
			raise InstallationError(_("A WordPress configuration file at %(file)s could not be created") % {'file': blog.config_file_path}, e)
		config_file.write(render_to_string('pressgang/install/wp/wp-config.php', {
			'db_name':       installer.db_name,
			'db_user':       installer.db_user,
			'db_password':   installer.db_password,
			'db_host':       installer.db_host,
			'blog_path':     blog.relative_url,
			'deletion_flag': self._DELETION_FLAG,
			'server_base':   _settings.SERVER_BASE,
			'version':       blog.version
		}))
		config_file.close()
		self.complete(_("WordPress configuration file created."))

		# Run the web-based installation script
		# TODO: make this a little more abstract to handle other versions
		self.start(_("Configuring WordPress."))
		try:
			response = urllib2.urlopen(
				blog.installation_url,
				urllib.urlencode({
					'weblog_title': blog.title.encode('utf-8'),
					'admin_password': installer.password.encode('utf-8'),
					'admin_password2': installer.password.encode('utf-8'),
					'admin_email': installer.admin_email.encode('utf-8'),
					'blog_public': int(installer.is_public)
				})
			)
		except (ValueError, httplib.HTTPException, urllib2.URLError), e:
			raise InstallationError(_("The WordPress installation page at %(url)s could not be loaded.") % {'url': blog.installation_url}, e)
		self.complete(_("WordPress successfully configured."))

		# If we're on a version that supports multisite, activate it
		if blog.version.is_multi:
			if blog.version.major == 3:
				self.start(_("Activating multisite."))
				self._activate_multisite(blog, installer)
				self.complete(_("Multisite activated."))

	def _activate_multisite(self, blog, installer):
		"""Enables multisite on a WordPress version that supports it.

		Arguments:
		blog -- an instance of a Blog object
		installer -- an instance of a BaseInstaller-descended object

		"""

		# Activate the network through the WordPress admin interface
		site_name = _("%(blog)s Blogs") % {'blog': blog.title}
		blog.make_admin_request(blog.network_activate_url, {
			'sitename': site_name.encode('utf-8'),
			'email': installer.admin_email
		})

		# Since the configuration file already contains the lines required to
		# activate multisite, simply remove the wrapping comments
		try:
			config = open(blog.config_file_path, 'r')
		except OSError, e:
			raise InstallationError(_("The WordPress config file at %(file)s could not be read.") % {'file': blog.config_file_path}, e)
		(temp_config_desc, temp_config_path) = tempfile.mkstemp()
		temp_config = os.fdopen(temp_config_desc, 'w')
		for line in config:
			if self._DELETION_FLAG not in line:
				temp_config.write(line)
		config.close()
		temp_config.close()

		# Overwrite the current config file with the modified multisite version
		try:
			shutil.copyfile(temp_config_path, blog.config_file_path)
		except OSError, e:
			raise InstallationError(_("The WordPress config file at %(file)s could not be updated to enable multisite mode.") % {'file': blog.config_file_path}, e)
		finally:
			os.remove(temp_config_path)

		# Update the blog's .htaccess file
		try:
			htaccess = open(blog.htaccess_path, 'w')
		except OSError, e:
			raise InstallationError(_("The Apache access file at %(file)s could not be updated to enable multisite.") % {'file': blog.htaccess_path}, e)
		htaccess.write(render_to_string('pressgang/install/wp/ms-htaccess.conf', {
			'blog_path': blog.relative_url
		}))
		htaccess.close()

		# Create the blogs.dir directory
		if not os.path.isdir(blog.blogs_dir_path):
			try:
				os.mkdir(blog.blogs_dir_path)
			except OSError, e:
				raise InstallationError(_("The blogs directory at %(dir)s could not be created.") % {'dir': blog.blogs_dir_path}, e)
