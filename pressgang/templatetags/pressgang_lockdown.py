
from django import template
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.lockdown.models import LockdownStatus
from pressgang.core.models import Blog

register = template.Library()

@register.filter
def is_locked(blog):
	"""Return True if the blog is locked down.

	If this is called on any object besides a Blog instance, an error is raised.

	Arguments:
	blog -- a Blog instance

	Returns: a boolean of whether or not the blog is locked down

	"""
	if not isinstance(blog, Blog):
		raise template.TemplateSyntaxError(_("The %(tag)s can only be called on a %(type)s instance.") % {'tag': 'is_locked', 'type': 'Blog'})
	return LockdownStatus.objects.is_blog_locked(blog)

