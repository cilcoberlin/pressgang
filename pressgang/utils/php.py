
import re

QUOTE_SEARCH = re.compile(r'([\'"])')

def _php_quote_string(value):
	"""Returns a properly quoted PHP string.

	Arguments:
	value -- a Python string

	Returns: a string of the quoted value of the Python string

	"""
	return "'%s'" % re.sub(QUOTE_SEARCH, r'\\\1', value)

def python_to_php(value):
	"""Cast the Python value as a PHP one.

	Arguments:
	value -- a value as a normal Python data type

	Returns: a string of how the value would appear in PHP code

	"""

	if isinstance(value, bool):
		php = "true" if value else "false"
	elif isinstance(value, int):
		php = value
	elif isinstance(value, list):
		php = "array(%s)" % ",".join([python_to_php(list_val) for list_val in value])
	elif isinstance(value, dict):
		php = "array(%s)" % ",".join([
			"%s => %s" % (_php_quote_string(key), python_to_php(val)) for key, val in value.iteritems()
		])
	else:
		php = _php_quote_string(value.strip())

	return php
