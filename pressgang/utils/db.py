
from django.utils.translation import ugettext as _

from pressgang.core.exceptions import PressGangConfigurationError
import pressgang.settings as _settings

import MySQLdb

def connect_to_db_as_admin( db=None ):
	"""Return a connection to the database server made as an admin user.

	The user should have enough privileges to create and drop databases.  Which
	user to connect as is determined by the DB_ADMIN_USER and DB_ADMIN_PASSWORD
	application settings values.  If the connection information is incorrect,
	a PressGangConfigurationError is raised.

	Keyword Arguments:
	db -- the name of a database to connect to

	Returns: a connection to the MySQL database as an admin

	"""
	kwargs = {
		'user': _settings.DB_ADMIN_USER,
		'passwd': _settings.DB_ADMIN_PASSWORD}
	if db:
		kwargs['db'] = db
	try:
		return MySQLdb.connect(**kwargs)
	except MySQLdb.OperationalError:
		raise PressGangConfigurationError(_("The database admin username and password specified in your %(file)s file are incorrect.") % {'file': 'settings.py'})
