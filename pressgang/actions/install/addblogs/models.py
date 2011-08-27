
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.models import ActionRecord

class BlogAdditionRecord(ActionRecord):
	"""A record of a blog having new sub-blogs created on it."""

	class Meta:
		app_label = "pressgang"
		verbose_name = _("blog addition record")
		verbose_name_plural = _("blog addition records")
