
from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from pressgang.utils.php import python_to_php

import random
import re
import string

register = template.Library()

@register.tag
def setter_function(parser, token):
	"""Generate a name for a setter function for a given value.

	This expects an argument of a string that will be used as the basis for
	the setter function name.

	Returns: the name of a function to set the value

	"""

	try:
		tag_name, arg = token.contents.split(None, 1)
	except ValueError:
		raise template.TemplateSyntaxError(_("%(tag)s tag requires a string as its only argument") % {'tag': 'setter_function'})

	m = re.search(r'(.*?) as (\w+)', arg)
	if not m:
		raise template.TemplateSyntaxError(_("%(tags)s tag has invalid arguments") % {'tag': tag_name })

	to_set, var_name = m.groups()
	return SetterFunctionNode(to_set, var_name)

class SetterFunctionNode(template.Node):
	"""Node for determining the name of a setter function."""

	def __init__(self, to_set, var_name):
		self.to_set = template.Variable(to_set)
		self.var_name = var_name

	def _make_setter_name(self, value):
		"""Generate a name for a setter function for a given value.

		Arguments:
		option -- the name of a value to set

		Returns: the name of a function to set the value

		"""
		return "_pressgang_setter_%(value)s_%(uid)s" % {
			'uid':   "".join(random.sample(string.ascii_letters, 20)),
			'value': value
		}

	def render(self, context):
		context[self.var_name] = self._make_setter_name(self.to_set.resolve(context))
		return ''

@register.filter
def as_php(value):
	"""Cast the Python value as a PHP one.

	Arguments:
	value -- a value as a normal Python data type

	Returns: a string of how the value would appear in PHP code

	"""
	return mark_safe(python_to_php(value))

@register.inclusion_tag('pressgang/options/unique_username.php')
def get_username(username, email):
	return {
		'email':    email,
		'username': username
	}

@register.simple_tag
def random_password():
	"""Generate a random password to use for a WordPress account."""
	return User.objects.make_random_password()
