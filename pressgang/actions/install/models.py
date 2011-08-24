
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.models import ActionRecord

class InstallationRecord(ActionRecord):
	"""A record of an installation."""

	class Meta:
		app_label = "pressgang"
		verbose_name = _("installation record")
		verbose_name_plural = _("installation records")
