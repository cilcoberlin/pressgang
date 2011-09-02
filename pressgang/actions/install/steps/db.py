
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.steps import InstallationStep
from pressgang.actions.install.exceptions import InstallationError
from pressgang.utils.constants import SAFE_ASCII
import pressgang.settings as _settings

import MySQLdb

class Step(InstallationStep):

	name = _("Database setup")

	# The maximum length for a username in MySQL
	_MYSQL_MAX_USERNAME_LENGTH = 16

	# The desired length of the MySQL user's password
	_MYSQL_PASSWORD_LENGTH = 30

	# Permissions required by a database user for WordPress to work
	_WP_REQUIRED_MYSQL_PERMISSIONS = [
		"SELECT",
		"INSERT",
		"UPDATE",
		"DELETE",
		"ALTER",
		"CREATE",
		"INDEX"
	]

	def execute(self, blog, installer):
		"""Creates a MySQL database and a user account for the current blog."""

		try:
			conn = MySQLdb.connect(
				user = _settings.DB_ADMIN_USER,
				passwd = _settings.DB_ADMIN_PASSWORD,
				charset = installer.db_charset)
		except MySQLdb.OperationalError, e:
			raise InstallationError(_("A connection to the database server could not be established."), e)
		else:
			cursor = conn.cursor()

		# Determine a unique database name for the blog to use, avoiding
		# conflicts with other databases via the addition of a numeric suffix
		valid_db = False
		db_count = 1
		db_base_name = installer.provide_db_base_name()
		while not valid_db:
			db_name = "_".join([db_base_name, str(db_count)])
			try:
				cursor.execute("USE %s" % db_name)
			except MySQLdb.OperationalError:
				valid_db = True
			else:
				db_count += 1

			# Prevent runaway database creation, which could happen if the
			# operational error is thrown for reasons unrelated to fetching
			# a nonexistent database
			if db_count > 1000:
				raise InstallationError(_("A suitable database name could not be determined."))

		# Determine an appropriate username for the database user, avoiding
		# conflicts with other users via the addition of a numeric suffix
		valid_user = False
		user_count = 1
		user_base_name = installer.provide_db_user_base_name()
		while not valid_user:
			suffix = "%s%d" % ("_", user_count)
			user_name = "%s%s" % (user_base_name[:self._MYSQL_MAX_USERNAME_LENGTH - len(suffix)], suffix)
			try:
				cursor.execute("SELECT COUNT(*) FROM mysql.user WHERE User=%s", (user_name,))
			except MySQLdb.OperationalError, e:
				raise InstallationError(_("A suitable database username could not be determined."), e)
			else:
				if cursor.fetchone()[0]:
					user_count += 1
				else:
					valid_user = True
		db_password = self._make_random_db_password()

		# Create the database and user, granting permissions required for
		# the proper functioning of WordPress
		self.start(_("Creating blog database."))
		try:
			cursor.execute("CREATE DATABASE %(db)s DEFAULT CHARACTER SET %(charset)s DEFAULT COLLATE %(collation)s" % {
				'db': db_name,
				'charset': installer.db_charset,
				'collation': installer.db_collation
			})
		except MySQLdb.OperationalError, e:
			raise InstallationError(_("A database could not be created."), e)
		self.complete(_("Blog database created."))
		self.start(_("Creating blog database user."))
		try:
			cursor.execute("GRANT %(permissions)s ON %(db)s.* TO '%(user)s'@'localhost' IDENTIFIED BY '%(password)s'" % {
				'permissions': ",".join(self._WP_REQUIRED_MYSQL_PERMISSIONS),
				'db': db_name,
				'user': user_name,
				'password': db_password})
		except MySQLdb.OperationalError, e:
			raise InstallationError(_("A database user could not be created"), e)
		cursor.execute("FLUSH PRIVILEGES")
		self.complete(_("Blog database user created."))

		# Store our database values for later use and clean up the connection
		installer.db_name = db_name
		installer.db_user = user_name
		installer.db_password = db_password
		cursor.close()
		conn.close()

	def _make_random_db_password(self):
		"""Generates a strong random password for the database user.

		Returns: a password to use for the database user
		"""
		return User.objects.make_random_password(self._MYSQL_PASSWORD_LENGTH, SAFE_ASCII)
