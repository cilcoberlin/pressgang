
from django.core.exceptions import ImproperlyConfigured

class PressGangConfigurationError(ImproperlyConfigured):
	"""A general error with PressGang's configuration."""
	pass

class PressGangError(Exception):
	"""A general error that occurred with PressGang."""
	pass
