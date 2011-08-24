
from pressgang.actions.exceptions import ActionError

class LockdownError(ActionError):
	"""An error that occurred during the locking or unlocking of a blog."""
	pass
