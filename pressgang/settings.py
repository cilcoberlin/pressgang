
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from pressgang.core.exceptions import PressGangConfigurationError

# The prefix that a user must use in their settings.py file before any variables
# that directly control a PressGang setting
_SETTINGS_PREFIX = "PRESSGANG_"

def _get_app_setting(setting):
	"""Get the value of the requested application setting.

	This searches first in the user's settings.py file, looking for the requested
	setting name prefixed with the app identifier.  If the value is not found,
	the passed default is used.

	Arguments:
	setting -- the name of the setting

	Returns: the value of the application setting

	"""
	return getattr(settings, "%s%s" % (_SETTINGS_PREFIX, setting), None)

def _setting_name(setting):
	"""Return the setting name as it would appear in a user's settings.py file.

	Returns: a string of the setting name as it would be in a settings.py file.

	"""
	return "settings.%s%s" % (_SETTINGS_PREFIX, setting)

# The absolute path to the directory that will contain per-blog Apache config files
APACHE_CONFIGS_DIR = _get_app_setting('APACHE_CONFIGS_DIR')
if not APACHE_CONFIGS_DIR:
	raise PressGangConfigurationError(_("You must provide the absolute path to the directory that will contain per-blog Apache configuration files via %(var)s.") % {'var': _setting_name('APACHE_CONFIGS_DIR')})

# The root directory from which Apache serves files
APACHE_DOCUMENT_ROOT = _get_app_setting('APACHE_DOCUMENT_ROOT')
if not APACHE_DOCUMENT_ROOT:
	raise PressGangConfigurationError(_("You must provide the value of Apache's DocumentRoot via %(var)s.") % {'var': _setting_name('APACHE_DOCUMENT_ROOT')})

# The command that will gracefully reload Apache
APACHE_RELOAD_CMD = _get_app_setting('APACHE_RELOAD_CMD')
if not APACHE_RELOAD_CMD:
	raise PressGangConfigurationError(_("You must provide the command that will gracefully reload Apache via %(var)s.") % {'var': _setting_name('APACHE_RELOAD_CMD')})

# The directory used for storing blog backups
BACKUPS_DIR = _get_app_setting('BACKUPS_DIR')
if not BACKUPS_DIR:
	raise PressGangConfigurationError(_("You must provide the absolute path to the directory that will contain blog backups via %(var)s.") % {'var': _setting_name('BACKUPS_DIR')})

# The password to go with the DB_ADMIN_USER admin username
DB_ADMIN_PASSWORD = _get_app_setting('DB_ADMIN_PASSWORD')
if not DB_ADMIN_PASSWORD:
	raise PressGangConfigurationError(_("You must provide the password of the MySQL admin user via %(var)s.") % {'var': _setting_name('DB_ADMIN_PASSWORD')})

# The username of a MySQL admin user
DB_ADMIN_USER = _get_app_setting('DB_ADMIN_USER')
if not DB_ADMIN_USER:
	raise PressGangConfigurationError(_("You must provide the username of the MySQL admin user via %(var)s.") % {'var': _setting_name('DB_ADMIN_USER')})

# Installation packages that can be extended by the user
INSTALLERS = [
	'pressgang.actions.install.installers.wp3',
	'pressgang.actions.install.installers.wp3ms'
]
INSTALLERS.extend(_get_app_setting('INSTALLERS') or [])

# The full path to the mysql executable
MYSQL_PATH = _get_app_setting('MYSQL_PATH')
if not MYSQL_PATH:
	raise PressGangConfigurationError(_("You must provide the full path to your mysql executable via %(var)s.") % {'var': _setting_name('MYSQL_PATH')})

# The full path to the mysqldump
MYSQLDUMP_PATH = _get_app_setting('MYSQLDUMP_PATH')
if not MYSQLDUMP_PATH:
	raise PressGangConfigurationError(_("You must provide the full path to your mysqldump executable via %(var)s.") % {'var': _setting_name('MYSQLDUMP_PATH')})

# The base HTTP address of the server
SERVER_BASE = _get_app_setting('SERVER_BASE')
if not SERVER_BASE:
	raise PressGangConfigurationError(_("You must provide the network location of your server via %(var)s.") % {'var': _setting_name('SERVER_BASE')})
