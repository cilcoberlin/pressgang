
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.models import ActionRecord

class ReversionRecord(ActionRecord):
	"""A record of a blog being reverted to a previous version snapshot."""

	class Meta:
		app_label = "pressgang"
		verbose_name = _("reversion record")
		verbose_name_plural = _("reversion records")
