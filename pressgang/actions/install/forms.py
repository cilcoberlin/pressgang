
from django import forms
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.fields import InstallerSelectField
from pressgang.core.fields import EmailListField

class InstallBlogForm(forms.Form):
	"""A form allowing the user to install a new blog."""

	slug = forms.SlugField(label=_("URL slug"), help_text=_("the last component of the blog's base URL"))
	title = forms.CharField(label=_("title"), help_text=_("the full title of the blog"))
	description = forms.CharField(label=_("description"), help_text=_("the blog's description / subtitle"))
	admins = EmailListField(label=_("admin emails"), help_text=_("a list of admin emails, one per line"))
	users = EmailListField(label=_("user emails"), help_text=_("a list of normal user emails, one per line"), required=False)
	password = forms.CharField(widget=forms.PasswordInput, label=_("admin password"), help_text=_("the admin password for the blog"))
	password_verify = forms.CharField(widget=forms.PasswordInput, label=_("admin password (verify)"), help_text=_("the admin password for the blog"))
	installer = InstallerSelectField(label=_("blog type"), help_text=_("the type of blog to install"))

	def clean(self):
		"""Verify formwide input."""

		data = self.cleaned_data

		# Verify that the two passwords match
		if data.get('password') != data.get('password_verify'):
			raise forms.ValidationError(_("The admin passwords must match."))

		return data

	def create_installer(self):
		"""Create an installer.

		Note that this can only be called if the form is valid.  Trying to
		call it when it is not valid will result in a number of errors.
		"""

		data = self.cleaned_data
		Installer = data['installer']
		return Installer(
			slug = data['slug'],
			title = data['title'],
			description = data['description'],
			admins = data['admins'],
			users = data['users'],
			password = data['password']
		)
