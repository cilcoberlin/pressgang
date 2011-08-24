
from django.utils.translation import ugettext_lazy as _

from pressgang.actions import Action
from pressgang.actions.revert.models import ReversionRecord
from pressgang.core.exceptions import PressGangError

class RevertAction(Action):
	"""An action for reverting a blog to a previous version snapshot."""

	display_name = _("reversion")

	Record = ReversionRecord

	log_template = "pressgang/revert/record.html"
	execute_template = "pressgang/revert/revert.html"

	steps = [
		'pressgang.actions.revert.steps.revert',
	]

	def __init__(self, *args, **kwargs):
		"""Create a new reversion action.

		Keyword Arguments:
		version -- the version of the blog to revert to

		"""
		self.snapshot = kwargs.pop('snapshot', True)
		super(RevertAction, self).__init__(*args, **kwargs)

	def on_success(self, blog):
		"""Update the blog's WordPress version once it has been reverted."""
		blog.version = self.snapshot.wp_version
		blog.save()
