
from django.utils.translation import ugettext_lazy as _

from pressgang.actions import Action
from pressgang.actions.lockdown.models import LockdownRecord
from pressgang.core.exceptions import PressGangError

class LockdownAction(Action):
	"""An action for locking or unlocking a WordPress blog.

	When a blog is put into lockdown, aggressive caching is applied to it,
	and commenting and other interactive features are disabled.
	"""

	display_name = _("lockdown")

	Record = LockdownRecord

	log_template = "pressgang/lockdown/record.html"
	execute_template = "pressgang/lockdown/lockdown.html"

	steps = [
		'pressgang.actions.lockdown.steps.interaction',
		'pressgang.actions.lockdown.steps.caching'
	]

	def __init__(self, *args, **kwargs):
		"""Create either a lockdown or unlock action.

		Keyword Arguments:
		lock -- whether or not to lock the blog down

		"""

		self.locking = kwargs.pop('lock', True)
		super(LockdownAction, self).__init__(*args, **kwargs)

		# Throw an error if the blog has already had the lockdown action
		# performed on it
		if self.blog.is_locked == self.locking:
			if self.locking:
				raise PressGangError(_("The blog %(blog)s is already locked down.") % {'blog': self.blog.title})
			else:
				raise PressGangError(_("The blog %(blog)s is already unlocked.") % {'blog': self.blog.title})

	def on_success(self, blog):
		"""Change the blog's lockdown state once the action has completed."""
		blog.is_locked = self.locking
		blog.save()
