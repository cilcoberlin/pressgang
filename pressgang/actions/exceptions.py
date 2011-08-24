
from django.utils.encoding import force_unicode

class ActionError(Exception):
	"""An error that occurred during the execution of an action on a blog."""

	def __init__(self, message, error_info = None):
		"""Creates a new exception.

		Arguments:
		message -- text describing the error
		error_info -- an optional Exception instance

		"""
		super(ActionError, self).__init__(force_unicode(message))
		self.error_info = error_info

