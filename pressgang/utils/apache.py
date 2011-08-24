
import pressgang.settings as _settings

import subprocess

def reload_apache():
	"""Gracefully reloads Apache's configuration files."""
	subprocess.call(_settings.APACHE_RELOAD_CMD.split(" "))
