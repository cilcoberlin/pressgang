
from pressgang.actions.install import InstallAction

class Install(InstallAction):
	"""Base installer for WordPress 3 running multisite."""

	display_name = "WordPress 3 Multisite"
	wp_version = "3.1"
	multiple_blogs = True
