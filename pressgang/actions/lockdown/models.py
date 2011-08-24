
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.models import ActionRecord

class LockdownRecord(ActionRecord):
	"""A record of a blog being placed into or taken out of lockdown."""

	class Meta:
		app_label = "pressgang"
		verbose_name = _("lockdown record")
		verbose_name_plural = _("lockdown records")
