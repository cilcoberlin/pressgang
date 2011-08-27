
from django import forms
from django.utils.translation import ugettext_lazy as _

from pressgang.core.fields import EmailListField
from pressgang.actions.install.fields import InstallerSelectField

class BlogAdditionForm(forms.Form):
	"""A form allowing a user to add sub-blogs to an existing blog."""

	blog_type = InstallerSelectField(label=_("blog type"), help_text=_("the type of child blog to create for each user"))
	users = EmailListField(label=_("user emails"), help_text=_("a list of user emails, one per line"))
