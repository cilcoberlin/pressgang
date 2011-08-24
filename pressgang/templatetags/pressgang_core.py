
from django import template
from django.contrib.humanize.templatetags.humanize import apnumber
from django.utils.translation import ungettext_lazy as _n

from pressgang.core.models import Blog

from titlecase import titlecase

register = template.Library()

@register.inclusion_tag("pressgang/core/form_field.html")
@register.simple_tag
def form_field(field):
	"""Render the given form field."""
	return {
		'field': field,
		'field_title': titlecase(unicode(field.label)),
		'is_required': field.field.required
	}

@register.simple_tag
def managed_blog_count():
	"""Displays text of how many blogs are being managed."""
	blog_count = Blog.objects.all().count()
	return _n(
		"Managing %(count)s WordPress blog",
		"Managing %(count)s WordPress blogs",
		blog_count) % {'count': '<span class="count">%s</span>' % apnumber(blog_count)}
