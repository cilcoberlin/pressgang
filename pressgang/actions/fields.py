
from django import forms

import datetime
import hashlib

class ActionIDField(forms.CharField):
	"""A hidden input that contains an action ID."""

	def __init__(self, *args, **kwargs):
		"""Create a new action ID field.

		Arguments:
		action -- the type of the action that should be identified

		"""

		# Make this a hidden widget with a pseudo-unique action identifier
		action = kwargs.pop('action', 'action')
		defaults = {
			'initial': self._generate_id(action),
			'widget': forms.HiddenInput
		}
		defaults.update(kwargs)
		super(ActionIDField, self).__init__(*args, **defaults)

	def _generate_id(self, action):
		"""Generate a pseudo-unique ID for the given action.

		Arguments:
		action -- a string of the action type

		Returns: a pseudo-unique action ID

		"""

		timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		md5 = hashlib.md5()
		md5.update(timestamp)
		return ".".join(["install", md5.hexdigest(), timestamp])
