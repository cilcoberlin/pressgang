
from django import forms
from django.utils.translation import ugettext_lazy as _

class ReversionForm(forms.Form):
	"""A form allowing a user to select which version to revert to."""

	def __init__(self, blog, *args, **kwargs):
		"""Create a version-selection form for the given blog.

		Arguments:
		blog -- a Blog instance

		"""
		super(ReversionForm, self).__init__(*args, **kwargs)

		# Create a choices field of all the reversions for the blog
		self.fields['snapshot'] = forms.ModelChoiceField(
			queryset=blog.version_snapshots.order_by('-created'),
			label=_("version"),
			error_messages={'required': _('You must select a version snapshot.')})
