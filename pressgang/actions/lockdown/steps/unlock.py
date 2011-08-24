
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.lockdown.steps import LockdownStep
from pressgang.actions.lockdown.exceptions import LockdownError

class Step(LockdownStep):

	name = _("Unlock blog")

	def execute(self, blog, lockdown):
		"""Bring the blog out of lockdown."""
		pass
