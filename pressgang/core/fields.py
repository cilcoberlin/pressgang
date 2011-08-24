
from django import forms
from django.utils.translation import ugettext_lazy as _

import re

class NewlineSeparatedTextField(forms.CharField):
	"""A field that accepts text input separated by newlines.

	The text data is split by newlines and then normalized  as a list of strings.
	"""

	_SEPARATOR = re.compile(r'[\r\n]{1,}')

	widget = forms.Textarea

	def clean(self, value):
		"""Parse the text as a list of newline-separated strings."""
		value = super(NewlineSeparatedTextField, self).clean(value)
		data = []
		if value:
			for line in re.split(self._SEPARATOR, value):
				if line:
					data.append(line.strip())
		return data

class EmailListField(NewlineSeparatedTextField):
	"""A field that expects text containing one email per line."""

	_VALID_EMAIL = re.compile(r'[a-zA-Z0-9_\-\.]+\@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+){1,}$')

	def clean(self, value):
		"""Verify that each value is a valid email address."""
		data = super(EmailListField, self).clean(value)
		for line in data:
			if not self._VALID_EMAIL.search(line):
				raise forms.ValidationError(_("%(value)s is not a valid email address.") % {'value': line})
		return data
