
from django import template
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from pressgang.utils.php import python_to_php

import datetime
import random
import string

register = template.Library()

def _create_pseudo_unique_function_name():
	"""Return the name of a pseudo-unique function in which to wrap the given code.

	Returns: a pseudo-unique function name.

	"""
	return "_pressgang_wrapper_%(date)s_%(uid)s" % {
		'date': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
		'uid': "".join(random.sample(string.ascii_letters, 20)),
	}

@register.tag
def safe_scope(parser, token):
	"""Wraps a block of PHP code in a function to avoid variable name clashes."""
	nodelist = parser.parse(('endsafe_scope',))
	parser.delete_first_token()
	return SafeScopeNode(nodelist)

class SafeScopeNode(template.Node):
	"""The node to render the safe_scope tag."""

	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		return self._wrap_code(self.nodelist.render(context))

	def _wrap_code(self, code):
		"""Wrap the given code in a self-calling function to prevent name clashes."""
		return render_to_string('pressgang/options/safe_scope.php', {
			'code': code,
			'function': _create_pseudo_unique_function_name()
		})

@register.tag
def execute_once(parser, token):
	"""Makes the PHP code wrapped in this block tag only execute once.

	Since the method that PressGang uses to set options is to simply create
	MU plugins for each bit of code that needs to be run, this makes sure that
	the code is not actually executed every time that a page is loaded.

	"""
	nodelist = parser.parse(('endexecute_once',))
	parser.delete_first_token()
	return ExecuteOnceNode(nodelist)

class ExecuteOnceNode(template.Node):
	"""The node to parse the execute_once tag."""

	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		return self._wrap_code(self.nodelist.render(context))

	def _wrap_code(self, code):
		"""Wraps the given code in a block that makes it execute only once."""
		return render_to_string('pressgang/options/execute_once.php', {
			'code': code,
			'function': _create_pseudo_unique_function_name()
		})

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
