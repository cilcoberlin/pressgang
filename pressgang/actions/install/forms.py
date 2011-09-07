
from django import forms
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.exceptions import InstallationError
from pressgang.actions.install.fields import InstallerSelectField
from pressgang.core.fields import BooleanRadioField, EmailListField

class InstallBlogForm(forms.Form):
	"""A form allowing the user to install a new blog."""

	slug = forms.SlugField(label=_("URL slug"), help_text=_("the last component of the blog's base URL"))
	title = forms.CharField(label=_("title"), help_text=_("the full title of the blog"))
	description = forms.CharField(label=_("description"), help_text=_("the blog's description / subtitle"))
	admins = EmailListField(label=_("admin emails"), help_text=_("a list of admin emails, one per line"), required=False)
	users = EmailListField(label=_("user emails"), help_text=_("a list of normal user emails, one per line"), required=False)
	password = forms.CharField(widget=forms.PasswordInput, label=_("admin password"), help_text=_("the admin password for the blog"))
	password_verify = forms.CharField(widget=forms.PasswordInput, label=_("admin password (verify)"), help_text=_("the admin password for the blog"))
	installer = InstallerSelectField(label=_("blog type"), help_text=_("the type of blog to install"))
	is_public = BooleanRadioField(label=_("blog visibility"), help_text=_("whether the blog is visible to search engines"), initial=0, true_text=_("public"), false_text=_("private"))

	def clean(self):
		"""Verify formwide input."""

		data = self.cleaned_data

		# Verify that the two passwords match
		if data.get('password') != data.get('password_verify'):
			raise forms.ValidationError(_("The admin passwords must match."))

		# Verify that the blog's installation path is available.  They KeyError
		# is caught because the form might not be entirely valid, and the
		# `create_installer` method expects it to be so, and thus have a value
		# for every key of the form's cleaned data.
		#
		# The InstallationError, in turn, is caught because that will be raised
		# when initializing an installer if the installation path is invalid.
		# While oddly structured, this code works this way due to the fact that
		# the installer provides the installation path dynamically, and can do
		# so only when it has all the values from this installation form.
		try:
			self.create_installer()
		except KeyError:
			pass
		except InstallationError, e:
			raise forms.ValidationError(e.message)

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
			password = data['password'],
			is_public = data['is_public'])
