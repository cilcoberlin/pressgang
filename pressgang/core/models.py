
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as __, ugettext_lazy as _

from pressgang.core.modelfields import EncryptedCharField
from pressgang.utils.constants import WP_ROLES
from pressgang.utils.db import connect_to_db_as_admin
from pressgang.utils.urls import url_join
from pressgang.utils.wp import TemporaryPlugin
import pressgang.settings as _settings

import cgi
import cookielib
import datetime
import lxml.html
import MySQLdb
import os
import re
import shutil
import subprocess
import time
import urllib
import urllib2

class WordPressVersionManager(models.Manager):
	"""Custom manager for the WordPressVersion class."""

	# The URL that returns the current version of wordpress
	_WP_VERSION_URL = "http://api.wordpress.org/core/version-check/1.1/"

	# The interval (in seconds) that must pass before checking for a new version
	_VERSION_CACHE_LENGTH = 60 * 60 * 24

	def get_from_string(self, version, is_multi=False):
		"""Get a WordPressVersion instance from the given version string.

		If there is not already an instance matching the string, a new one
		is created by parsing the string.

		Arguments:
		version -- a string specifying a WordPress version, such as "3.1"
		is_multi -- an optional boolean specifying whether the version is WPMU / multisite

		Returns: a WordPressVersion instance of the version

		"""
		try:
			version = self.get(full=version, is_multi=is_multi)
		except self.model.DoesNotExist:
			version = self.create(full=version, is_multi=is_multi)
		return version

	def _check_current_version(self):
		"""Create instances for the current stable version of WordPress."""

		# If the update interval has yet to expire, don't check
		if cache.get('version_checked'):
			return

		# Get the current version from WordPress
		try:
			response = urllib2.urlopen(self._WP_VERSION_URL)
		except urllib2.URLError:
			return
		else:
			parts = response.read().split('\n')
			try:
				version = parts[2]
			except IndexError:
				return
			else:
				self.get_from_string(version, is_multi=False)
				self.get_from_string(version, is_multi=True)
				cache.set('version_checked', True, self._VERSION_CACHE_LENGTH)

	def current_version(self, multi=False):
		"""Get the current version of WordPress.

		Keyword Arguments:
		multi -- whether or not to return the WPMU / multisite current version

		Returns: the most recent WordPressVersion instance or None if no versions exist

		"""
		self._check_current_version()
		try:
			return self.filter(is_multi=multi).order_by('-major', '-minor')[0]
		except IndexError:
			return None

class WordPressVersion(models.Model):
	"""A version of WordPress."""

	objects = WordPressVersionManager()

	full     = models.CharField(max_length=10, verbose_name=_("full version"))
	major    = models.PositiveSmallIntegerField(verbose_name=_("major version number"))
	minor    = models.PositiveSmallIntegerField(verbose_name=_("minor version number"), default=0)
	is_multi = models.BooleanField(verbose_name=_("is WPMU / multisite enabled"))

	_NON_NUMBER_SEARCH = re.compile(r'[^0-9]')

	# The base URL from which all WordPress versions are available
	_WP_DOWNLOAD_URL = "http://wordpress.org"

	class Meta:

		app_label = "pressgang"
		verbose_name = _("WordPress version")
		verbose_name_plural = _("WordPress versions")

	def __unicode__(self):
		parts = [self.full]
		if self.is_multi:
			if self.major < 3:
				parts.append(__("MU"))
			else:
				parts.append(__("multisite"))
		return " ".join(parts)

	def save(self, *args, **kwargs):
		"""Save more detailed version information."""

		# Save the major and minor version numbers, determined from the version string
		if not self.major:
			versions = self._parse_version_string(self.full)
			self.major = versions[0]
			try:
				self.minor = versions[1]
			except IndexError:
				pass
		super(WordPressVersion, self).save(*args, **kwargs)

	def _parse_version_string(self, version):
		"""Determine the major and minor version parts from a string.

		Arguments:
		version -- a version string, such as "3.1"

		Returns: a tuple of ints of the form (major, minor)

		"""
		return [re.sub(self._NON_NUMBER_SEARCH, '', part) for part in version.split('.')[:2]]

	@property
	def download_url(self):
		"""The URL from which the version can be downloaded."""

		# Download the WPMU version of WordPress for pre-3.0 sites that should
		# support multiple blogs
		version_parts = ['wordpress']
		if self.is_multi:
			if self.major < 3:
				version_parts.append("mu")
		version_parts.append(self.full)

		return "%(base)s/%(version)s.zip" % {
			'base': self._WP_DOWNLOAD_URL.rstrip('/'),
			'version': "-".join(version_parts)
		}

class BlogManager(models.Manager):
	"""Custom manager for the Blog model."""

	def sync_blogs(self, interactive=False):
		"""Build a list of all blogs installed on the server.

		Keyword Arguments:
		interactive -- whether or not the method is being called at a prompt

		"""

		# Get a list of all directories on the server containing blogs.  This
		# attempts to speed things up by ignoring any child directories of a
		# directory that contains a blog, unless that directory is the root dir.
		blogs = []
		for root, dirs, files in os.walk(_settings.APACHE_DOCUMENT_ROOT):
			if self._path_contains_blog(root, files):
				blogs.append(root)
				if root != _settings.APACHE_DOCUMENT_ROOT:
					dirs[:] = []

		# Sync the current blog list with what we just found, ignoring any
		# blogs that are in the process of being installed
		self._prune_blogs()
		for blog_dir in blogs:
			try:
				blog = self.get(path=blog_dir)
			except Blog.DoesNotExist:
				blog = Blog(path=blog_dir)
			if blog.is_valid:
				if interactive:
					if blog.pk:
						print _("Updating blog at %(path)s") % {'path': blog_dir}
					else:
						print _("Creating blog at %(path)s") % {'path': blog_dir}
				blog.update_values()

	def _prune_blogs(self):
		"""Remove any blogs that are no longer on the server.

		Returns: a list of the PKs of any deleted blogs

		"""
		deleted = []
		blogs = list(self.all())
		for blog in blogs:
			if not blog.is_valid:
				deleted.append(blog.pk)
				blog.delete()
		return deleted

	def _path_contains_blog(self, dir, files=None):
		"""Return True if the given directory contains a WordPress blog.

		Arguments:
		dir -- the full path to a directory in which a WordPress blog might reside

		Keyword Arguments:
		files -- an optional list of files in the directory

		Returns: True if the directory hold a blog, False otherwise

		"""
		dir_files = files or os.listdir(dir)
		return Blog.WP_CONFIG_FILE in dir_files

	def list_by_path(self):
		"""List all blogs, ordered by path.

		Returns: a Blog queryset, ordered by the path

		"""
		return self.all().order_by('path')

	def list_by_date(self):
		"""List all blogs, ordered by their creation date.

		Returns: a Blog queryset, ordered by date

		"""
		return self.all().order_by('-created')

class Blog(models.Model):
	"""An installed WordPress blog."""

	objects = BlogManager()

	path    	   = models.CharField(max_length=255, verbose_name=_("path to directory"), unique=True)
	title   	   = models.CharField(max_length=255, verbose_name=_("display name"))
	version 	   = models.ForeignKey(WordPressVersion, verbose_name=_("WordPress version"))
	created        = models.DateTimeField(verbose_name=_("installation date and time"))
	admin_user     = models.CharField(max_length=40, verbose_name=_("the name of the administrator account"), null=True, blank=True)
	admin_password = EncryptedCharField(verbose_name=_("administrator password"), null=True, blank=True)
	is_managed     = models.BooleanField(verbose_name=_("is managed by PressGang"), default=False)

	# The name of the WordPress configuration file
	WP_CONFIG_FILE = "wp-config.php"

	# The name of the WordPress login file
	_WP_LOGIN_FILE = "wp-login.php"

	# The path to the WordPress network activation page
	_WP_NETWORK_ACTIVATION_PATH = "wp-admin/network.php"

	# The name of the WordPress content directory
	_WP_CONTENT_DIR = "wp-content"

	# The path to the blogs directory used in multisite mode
	_WP_BLOGS_DIR_PATH = "wp-content/blogs.dir"

	# Patterns for settings defined in the WordPress config file
	_WP_CONFIG_DEFINE_SETTING = re.compile(r'^define\((\s+)?[\'"](?P<setting>[A-Z_]+)[\'"](\s+)?,(\s+)?(?P<value>.+)\);\s+((//|/\*).*)?$')
	_WP_CONFIG_VAR_SETTING    = re.compile(r'^\$(?P<setting>[^\s]+)(\s+)?=(\s+)?(?P<value>.+);\s+((//|/\*).*)?$')

	# Directories that can contain user content inside of the wp-content directory
	WP_CONTENT_DIRS = [
		"plugins",
		"mu-plugins",
		"themes"
	]

	# Pattern for a cookie setting the user as logged in
	_WP_ADMIN_LOGGED_IN_COOKIE = re.compile(r'wordpress_logged_in_')

	# Patterns for the names of nonce and referer inputs on admin pages
	_WP_ADMIN_SECURITY_FIELD = re.compile(r'^_wp(.+)?(nonce|referer)')

	# The default database table prefix used by WordPress
	_WP_DEFAULT_TABLE_PREFIX = "wp_"

	# A mappingn of PressGang's names for WordPress tables to their actual names
	_WP_TABLE_NAMES = {
		'options': 'options'
	}

	# Table names that refer to settings for a blog, as opposed to sitewide settings
	_WP_BLOG_TABLE_NAMES = [
		'options'
	]

	# The name of a file that acts as a flag that the blog is managed by PressGang
	_MANAGEMENT_FLAG = ".pressgang"

	class Meta:

		app_label = "pressgang"
		verbose_name = _("blog")
		verbose_name_plural = _("blogs")

		permissions = (
			("can_install_blogs", __("Can install blogs")),
			("can_view_blogs", __("Can view a list of installed blogs")),
			("can_manage_blogs", __("Can apply changes to blogs"))
		)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		"""Make sure that the database is coherent with the blog's file structure."""

		# If the blog is marked as managed but does not have a management flag
		# created, make the flag file now, provided that the directory containing
		# the flag file exists, which will not be the case when the blog is
		# first being installed.
		management_flag = self._get_management_flag_path()
		if self.is_managed and not self._get_current_managed_status():
			if os.path.isdir(os.path.dirname(management_flag)):
				open(management_flag, 'w').close()

		super(Blog, self).save(*args, **kwargs)

	@property
	def is_valid(self):
		"""True if the blog's path and database both exist."""
		valid = os.path.isdir(self.path)
		if valid:
			db_conn = self._connect_to_db()
			if db_conn:
				valid = True
				db_conn.close()
			else:
				valid = False
		return valid

	@property
	def wp_content_path(self):
		"""The path to the blog's content directory."""
		return os.path.join(self.path, self._WP_CONTENT_DIR)

	@property
	def url(self):
		"""The URL at which the blog can be accessed."""
		return url_join("http://%s" % _settings.SERVER_BASE, self.relative_url)

	@property
	def relative_url(self):
		"""The URL of the blog relative to the server base."""
		address = self.path.replace(_settings.APACHE_DOCUMENT_ROOT, "")
		address = address.replace(os.sep, '/')
		return url_join(address)

	@property
	def relative_url_slashes(self):
		"""The relative URL of the blog with initial and trailing slashes."""
		url = self.relative_url
		return "%s%s%s" % ('/' * (not url.startswith('/')), url, '/' * (not url.endswith('/')))

	@property
	def admin_page_url(self):
		"""The absolute URL to the admin page base."""
		return url_join(self.url, 'wp-admin/')

	@property
	def network_admin_page_url(self):
		"""The absolute URL to the network admin page base."""
		return url_join(self.url, 'wp-admin', 'network/')

	@property
	def config_file_path(self):
		"""The path to the installation's PHP config file."""
		return os.path.join(self.path, self.WP_CONFIG_FILE)

	@property
	def version_file_path(self):
		"""The path to the installation's PHP version definition file."""
		return os.path.join(self.path, 'wp-includes', 'version.php')

	@property
	def installation_url(self):
		"""The absolute URL of the first-time installation page."""
		if self.version.major < 3:
			file = "index.php"
		else:
			file = "wp-admin/install.php?step=2"
		return url_join(self.url, file)

	@property
	def login_url(self):
		"""The URL of the login page."""
		return url_join(self.url, self._WP_LOGIN_FILE)

	@property
	def network_activate_url(self):
		"""The network activation page URL."""
		return url_join(self.url, self._WP_NETWORK_ACTIVATION_PATH)

	@property
	def plugins_path(self):
		"""The full path to the plugins folder."""
		return os.path.join(self.wp_content_path, "plugins")

	@property
	def mu_plugins_path(self):
		"""The full path to the MU plugins folder."""
		return os.path.join(self.wp_content_path, "mu-plugins")

	@property
	def htaccess_path(self):
		"""The full path to the blog's .htaccess file."""
		return os.path.join(self.path, '.htaccess')

	@property
	def blogs_dir_path(self):
		"""The full path to the blogs dir used when hosting multiple blogs."""
		return os.path.join(self.path, self._WP_BLOGS_DIR_PATH)

	@property
	def add_user_url(self):
		"""The absolute URL to the add-user page."""
		return url_join(self.admin_page_url, 'user-new.php')

	@property
	def config(self):
		"""A dict made from the DEFINE values in the blog's config file."""
		if not hasattr(self, '_config'):
			self._config = self._parse_config_file(self.config_file_path)
		return self._config

	@property
	def title_as_link(self):
		"""The title of the blog wrapped in an HTML link, safe for use in templates."""
		return mark_safe('<a href="%(href)s" class="blog-link">%(title)s</a>' % {
			'href': cgi.escape(self.url, quote=True),
			'title': cgi.escape(self.title)
		})

	@property
	def apache_conf_path(self):
		"""The path to the blog's Apache configuration file."""
		return os.path.join(
			_settings.APACHE_CONFIGS_DIR,
			"%s.conf" % "-".join(self.path[1:].split(os.sep)))

	@property
	def db_name(self):
		"""The name of the database used by the blog."""
		return self._get_db_info()['db_name']

	@property
	def has_version_snapshots(self):
		"""Whether or not the blog has any version snapshots."""
		return self.version_snapshots.count() > 0

	@property
	def most_recent_backup(self):
		"""The most recent version snapshot or None."""
		try:
			return self.version_snapshots.order_by('-created')[0]
		except IndexError:
			return None

	def wp_table(self, name, wpmu=False):
		"""Return the name of a WordPress table

		Arguments:
		name -- the internal name of the table

		Keyword Arguments:
		wpmu -- whether or not the table should be made in the old WPMU style

		Returns: the full WordPress table name

		"""

		parts = [self._get_db_info()['prefix']]

		# Since older WPMU versions stored options for the root blog as one
		# of its enumerated blog tables (wp_1_options vs wp_options), add in the
		# prefix if we're requesting one of those table for WPMU
		if wpmu and name in self._WP_BLOG_TABLE_NAMES:
			parts.append("1_")

		parts.append(name)
		return "".join(parts)

	def _get_management_flag_path(self):
		"""Get the path of the PressGang management flag file.

		Returns: the full path to the PressGang management flag file

		"""
		return os.path.join(self.wp_content_path, self._MANAGEMENT_FLAG)

	def update_values(self):
		"""Update the blog's values based on the current database and files."""
		self.version = self._get_current_version()
		self.title = self._get_current_title()
		self.created = self._get_current_created()
		self.is_managed = self._get_current_managed_status()
		self.save()
		self.create_standalone_apache_conf()

	def _get_current_managed_status(self):
		"""Get the current management status of the blog.

		Returns: a bool of the current management status.

		"""
		return os.path.isfile(self._get_management_flag_path())

	def _get_current_title(self):
		"""Get the title of the blog based on the title's database value.

		Returns: the current title of the blog as a string

		"""
		return self._wpdb_get_blog_option('blogname')

	def _get_current_version(self):
		"""Get the version based on the blog's current file structure.

		Returns: a WordPressVersion instance of the current version

		"""
		version = self._parse_config_file(self.version_file_path)
		config = self._parse_config_file(self.config_file_path)
		return WordPressVersion.objects.get_from_string(
			version['wp_version'],
			is_multi=config.get('MULTISITE', True) or 'wpmu_version' in version)

	def _get_current_created(self):
		"""Get the creation timestamp based on the blog's file structure.

		This uses the creation time of the config file to get a timestamp.

		Returns: a datetime timestamp of the blog's creation time

		"""
		return datetime.datetime.strptime(
			time.ctime(os.path.getctime(self.path)),
			"%a %b %d %H:%M:%S %Y")

	def create_standalone_apache_conf(self):
		"""Creates a standalone Apache configuration file for the blog."""
		conf_file_path = self.apache_conf_path
		if not os.path.isfile(conf_file_path):
			conf_file = open(conf_file_path, 'w')
			conf_file.write(render_to_string('pressgang/install/apache/blog.conf', {'blog_path': self.path}))
			conf_file.close()

	def _wpdb_get_blog_option(self, name):
		"""Return the value of an option for the main blog as stored in the database.

		Arguments:
		name -- the name of the option

		Returns: the option's value, or None if it is not set

		"""
		conn = self._connect_to_db()
		cursor = conn.cursor()

		# Since some older versions of WPMU stored blog options in an enumerated
		# table, try getting our value from both the wp_options and wp_1_options
		# tables, since one should exist
		tables = [self.wp_table('options')]
		if self.version.is_multi:
			tables.append(self.wp_table('options', wpmu=True))
		for table in tables:
			try:
				cursor.execute("SELECT option_value FROM " + table + " WHERE option_name=%s", (name,))
			except MySQLdb.ProgrammingError:
				pass
			else:
				value = cursor.fetchone()
				break

		cursor.close()
		conn.close()
		try:
			return value[0]
		except IndexError:
			return None

	def _connect_to_db(self):
		"""Establish a connection to the blog's database.

		Returns: a connection to the blog's database or None if the connection failed

		"""
		db_info = self._get_db_info()
		try:
			return MySQLdb.connect(
				db = db_info['db_name'] or "",
				user = db_info['user'] or "",
				passwd = db_info['password'] or "",
				host = db_info['host'] or "",
				charset = db_info['charset'] or "",
				use_unicode = True
			)
		except MySQLdb.Error:
			return None

	def _get_db_info(self):
		"""Get information on the database connection information for the blog.

		The keys available in the dict of info are as follows:

			charset  - the database's character set
			db_name  - the name of the database used
			host     - the database host
			password - the password that goes with the username
			prefix   - the datbase table prefix
			user     - the username with access to the database

		Returns: a dict containing database info

		"""
		config = self.config
		return {
			'charset':  config.get('DB_CHARSET'),
			'db_name':  config.get('DB_NAME'),
			'host':     config.get('DB_HOST'),
			'password': config.get('DB_PASSWORD'),
			'prefix':   config.get('table_prefix', self._WP_DEFAULT_TABLE_PREFIX),
			'user':     config.get('DB_USER')
		}

	def _parse_config_file(self, file):
		"""Get the values of settings in a WordPress configuration file.

		These values are returned as a dict whose keys will match the values
		of the define constants in the configuration file.

		Returns: a dict of the WordPress config file settings

		"""

		# Read each line of the config file, searching for settings
		config = {}
		config_file = open(file, 'r')
		for line in config_file:
			define_matches = self._WP_CONFIG_DEFINE_SETTING.search(line)
			var_matches = self._WP_CONFIG_VAR_SETTING.search(line)
			if define_matches:
				config[define_matches.group('setting')] = define_matches.group('value')
			if var_matches:
				config[var_matches.group('setting')] = var_matches.group('value')
		config_file.close()

		# Return the config values cast as Python types
		for key in config.keys():
			config[key] = self._parse_config_value_type(config[key])
		return config

	def _parse_config_value_type(self, value):
		"""Determine the proper type for the value defined in the wp-config file.

		The `value` passed will be the raw string occuring in the PHP file.  A
		value surrounded by quotes will be returned as a string, a bar number
		will be returned as an int, and a "true" or "false" string will be
		returned as the correct boolean type.

		Arguments:
		value -- the raw string for the value occurring in the wp-config file

		Returns: the value cast as a fitting data type

		"""
		value = value.strip()
		if value.startswith('"') or value.startswith("'"):
			return value[1:-1]
		elif value == 'true':
			return True
		elif value == 'false':
			return False
		else:
			try:
				return int(value)
			except ValueError:
				return value

	def create_plugin_file(self):
		"""Creates a temporary MU plugin that can be used to change blog settings.

		Returns: an instance of a TemporaryPlugin object

		"""

		# Return a reference to the plugin in the MU plugins directory
		if not os.path.isdir(self.mu_plugins_path):
			os.mkdir(self.mu_plugins_path)
		return TemporaryPlugin(self.mu_plugins_path)

	def apply_changes(self, php_code):
		"""Applies the changes defined in the given PHP code to the blog.

		This works by creating a temporary MU plugin file, writing the PHP code
		to it, and then loading the base admin page to execute the code.

		Arguments:
		php_code -- PHP code for altering the WordPress blog

		"""

		# Write the PHP code to a temporary plugin file
		plugin = self.create_plugin_file()
		plugin.write(php_code)

		# Request the base admin page to execute the code and clear the plugin
		self.make_admin_request(
			self.network_admin_page_url if self.version.is_multi else self.admin_page_url)
		plugin.remove()

	def _make_login_request(self, username, password):
		"""Perform a request to log the user in.

		Arguments:
		username -- the admin username
		password -- the admin password

		Returns: the urllib2 opener linked with the admin cookie

		"""

		# Initialize a cookie-aware URL opener
		cookie_jar = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
		urllib2.install_opener(opener)

		# Authenticate as the administrator
		login_data = {
			'log': username.encode('utf-8'),
			'pwd': password.encode('utf-8'),
			'rememberme': 1
		}
		response = opener.open(self.login_url, urllib.urlencode(login_data))
		response.close()
		return opener

	def is_admin_login(self, username, password):
		"""Check if the given username and password are for a valid admin.

		Arguments:
		username -- the username of a suspected admin user
		password -- the password for the given username

		Returns: True if the login is valid, False otherwise

		"""

		# Test if the user is an admin by first logging in and then attempting
		# to access the base administrative page
		self._make_login_request(username, password)
		response = urllib2.urlopen(self.admin_page_url)
		is_valid = response.geturl() == self.admin_page_url
		response.close()
		return is_valid

	def make_admin_request(self, url, data=None):
		"""Request the given admin page.

		This first logs in as the admin user, then requests the page.  If there
		is any data being sent, the page is first obtained via a GET request,
		the response text of which is used to get the nonce and referer value.
		After this is obtained, the actual request is performed.

		Arguments:
		url -- a string of the URL to request
		data -- an optional dict of POST parameters

		Returns: the text of the response

		"""

		opener = self._make_login_request(self.admin_user, self.admin_password)

		# If the request contains POST data, get the nonce and referer from the
		# page to which the request will be made and add it to the POST data
		if data:
			response = opener.open(url)
			page = lxml.html.document_fromstring(response.read())
			for form in page.forms:
				for field, value in form.fields.iteritems():
					if self._WP_ADMIN_SECURITY_FIELD.search(field):
						data[field] = value

		# Make the user request
		request_args = [url]
		if data:
			request_args.append(urllib.urlencode(data))
		response = opener.open(*request_args)
		response_text = response.read()
		response.close()
		return response_text

	def add_user(self, username, email, role=None):
		"""Add a user with the given role to the blog.

		If this is called for a WPMU or multisite blog, the user is added
		to the root blog, but does not have a blog created for them.

		Arguments:
		username -- the user's username
		email -- the user's email address
		role -- a string indicating the user's role

		"""

		if not role:
			role = WP_ROLES['contributor']

		self.apply_changes(
			render_to_string('pressgang/options/add_user.php', {
				'email':    email,
				'role':     role,
				'username': username
			})
		)

	def add_admin(self, username, email):
		"""Add a user as an admin on the blog.

		If this is called for a WPMU or multisite blog, the user is added
		as an admin on the root blog.

		Arguments:
		username -- the user's username
		email -- the admin's email address

		"""
		self.add_user(username, email, role=WP_ROLES['administrator'])

	def create_blog_for_user(self, username, email, blog_id, blog_title):
		"""Create a blog for the user on a WPMU or multisite blog.

		If this function is called on a blog that is not WPMU or multisite,
		it has no effect.

		Arguments:
		username -- the user's username
		email -- the user's email address
		blog_id -- the URL stub at which the blog can be accessed
		blog_title -- the title for the new blog

		"""
		if not self.version.is_multi:
			return
		self.apply_changes(
			render_to_string('pressgang/options/create_blog.php', {
				'blog':     self,
				'blog_id':  blog_id,
				'email':    email,
				'domain':   _settings.SERVER_BASE,
				'path':     url_join(self.relative_url, "%s"),
				'title':    blog_title,
				'username': username
			})
		)

	def fix_child_blog_permalinks(self):
		"""Fixes the permalinks on all of the child blogs on a site.

		This is required because the permalink structure of the child blogs is
		often set to mirror that of the root blog.

		"""
		self.apply_changes(render_to_string('pressgang/options/fix_permalinks.php'))

class VersionSnapshotManager(models.Manager):
	"""Custom manager for the VersionSnapshot model."""

	def new_snapshot(self, blog, reason=None):
		"""Create a new version snapshot of the given blog.

		Arguments:
		blog -- a Blog instance

		Keyword Arguments:
		reason -- an optional string describing why the snapshot is being taken

		Returns: a new VersionSnapshot instance

		"""
		version = self.create(blog=blog, wp_version=blog.version, reason=reason)
		try:
			version.take_snapshot()
		except Exception, e:
			version.delete()
			raise e
		return version

class VersionSnapshot(models.Model):
	"""A snapshot of a version of an installed blog.

	This model is primarily used to allow for rollbacks if an action cannot
	be completed successfully.  This snapshot stores all database information
	and files associated with a blog at a given point in time.
	"""

	objects = VersionSnapshotManager()

	blog       = models.ForeignKey(Blog, verbose_name=_("blog"), related_name="version_snapshots")
	wp_version = models.ForeignKey(WordPressVersion, verbose_name=_("WordPress version"))
	created    = models.DateTimeField(auto_now_add=True, verbose_name=_("creation timestamp"))
	reason     = models.TextField(verbose_name=_("reason for creating the version snapshot"), blank=True, null=True)

	# The names of stored files
	_APACHE_FILE_NAME = "blog.conf"
	_DB_FILE_NAME = "blog.sql"

	class Meta:

		app_label = "pressgang"
		verbose_name = _("version snapshot")
		verbose_name_plural = _("version snapshots")

	def __unicode__(self):
		return _("%(blog)s (%(date)s)") % {'blog': self.blog, 'date': self.created}

	@property
	def db_files_dir(self):
		"""The directory containing database files."""
		return os.path.join(self._get_backup_dir(), 'db')

	@property
	def blog_files_dir(self):
		"""The directory containing blog files."""
		return os.path.join(self._get_backup_dir(), 'blog')

	@property
	def apache_files_dir(self):
		"""The directory containing Apache files."""
		return os.path.join(self._get_backup_dir(), 'apache')

	@property
	def apache_conf_path(self):
		"""The full path to the backed up Apache config file for the blog."""
		return os.path.join(self.apache_files_dir, self._APACHE_FILE_NAME)

	def take_snapshot(self):
		"""Take a version snapshot of the blog."""
		self.prepare_for_snapshot()
		self.take_db_snapshot()
		self.take_blog_snapshot()
		self.take_apache_snapshot()

	def revert(self):
		"""Revert to this version snapshot of the blog."""
		self.revert_db()
		self.revert_blog_files()
		self.revert_apache_files()

	def delete(self, *args, **kwargs):
		"""Delete the version's files when deleting the version."""
		try:
			shutil.rmtree(self._get_backup_dir())
		except OSError, e:
			if settings.DEBUG:
				raise e
			pass
		super(VersionSnapshot, self).delete(*args, **kwargs)

	def prepare_for_snapshot(self):
		"""Prepare directories for taking a snapshot."""
		backup_dir = self._get_backup_dir()
		if os.path.isdir(backup_dir):
			shutil.rmtree(backup_dir)
		os.makedirs(backup_dir)

	def take_db_snapshot(self):
		"""Take a text snapshot of the blog's database.

		The snapshot of the database is an SQL dump as generated by mysqldump.
		"""
		os.mkdir(self.db_files_dir)
		db_file = open(os.path.join(self.db_files_dir, self._DB_FILE_NAME), 'w')
		subprocess.call(
			[_settings.MYSQLDUMP_PATH, '-u', _settings.DB_ADMIN_USER, '-p%s' % _settings.DB_ADMIN_PASSWORD, self.blog.db_name],
			stdout=db_file)
		db_file.close()

	def take_blog_snapshot(self):
		"""Take a snapshot of the blog's files."""
		shutil.copytree(self.blog.path, self.blog_files_dir)

	def take_apache_snapshot(self):
		"""Take a snapshot of the blog's Apache configuration file."""
		apache_conf = self.blog.apache_conf_path
		if os.path.isfile(apache_conf):
			os.mkdir(self.apache_files_dir)
			shutil.copyfile(apache_conf, self.apache_conf_path)

	def revert_db(self):
		"""Revert the database."""

		# Drop all tables on the blog's database to prevent the presence of
		# undeleted child blog tables interfering with the addition of blogs
		# after the reversion.  Since the database dump might not have the tables
		# used by child blogs added after it was created, it does not delete them.
		# This can cause a situation where a reverted blog has only two blogs,
		# but tables for more than that.  When a user tries to create a new blog,
		# WordPress sees that the tables required already exist, which prevents
		# it from actually creating the blog.
		conn = connect_to_db_as_admin(db=self.blog.db_name)
		cursor = conn.cursor()
		cursor.execute("SHOW TABLES")
		tables = [result[0] for result in cursor.fetchall()]
		for table in tables:
			cursor.execute("DROP TABLE %s" % table)
		cursor.close()
		conn.close()

		# Use the mysql executable to read in from the database dump
		db_file = open(os.path.join(self.db_files_dir, self._DB_FILE_NAME))
		call_args = self._mysql_call_args(_settings.MYSQL_PATH)
		subprocess.call(call_args, stdin=db_file)
		db_file.close()

	def revert_blog_files(self):
		"""Replace the blog's files with those of this version."""
		shutil.rmtree(self.blog.path)
		shutil.copytree(self.blog_files_dir, self.blog.path)

	def revert_apache_files(self):
		"""Revert to this version's Apache configuration files."""
		backup_conf = self.apache_conf_path
		if os.path.isfile(backup_conf):
			shutil.copyfile(backup_conf, self.blog.apache_conf_path)

	def _mysql_call_args(self, command, db=True):
		"""Generate the arguments for running the given MySQL command as an admin.

		Arguments:
		command -- the full path to a MySQL executable

		Keyword Arguments:
		db -- whether or not to include the blog's database as the last argument

		Returns: a list of commands suitable for passing to subprocess.call

		"""
		args = [
			command,
			'-u', _settings.DB_ADMIN_USER,
			'-p%s' % _settings.DB_ADMIN_PASSWORD]
		if db:
			args.append(self.blog.db_name)
		return args

	def _get_backup_dir(self):
		"""Get the base directory in which this version's files are stored.

		Returns: a path to the base backups directory

		"""
		return os.path.join(_settings.BACKUPS_DIR, "%06d" % self.blog.pk, "%06d" % self.pk)
