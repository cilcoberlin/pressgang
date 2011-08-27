
from django.utils.translation import ugettext as _

from pressgang.core.exceptions import PressGangConfigurationError
import pressgang.settings as _settings

import MySQLdb

def connect_to_db_as_admin():
	"""Return a connection to the database server made as an admin user.

	The user should have enough privileges to create and drop databases.  Which
	user to connect as is determined by the DB_ADMIN_USER and DB_ADMIN_PASSWORD
	application settings values.

	If a connection cannot be made, a PressGangConfigurationError is raised.
	"""
	try:
		return MySQLdb.connect(
			user = _settings.DB_ADMIN_USER,
			passwd = _settings.DB_ADMIN_PASSWORD
		)
	except MySQLdb.OperationalError:
		raise PressGangConfigurationError(_("The database admin username and password specified in your %(file)s file are incorrect.") % {'file': 'settings.py'})
