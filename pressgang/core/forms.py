
from django import forms
from django.utils.translation import ugettext_lazy as _

class AdminLoginInfoForm(forms.Form):
	"""A form that allows a user to provide login info for a WordPress admin account.

	This is used to associate login information with a blog found on the site.
	Since there is no direct way to determine the admin user and password from
	the files and database associated with a blog, PressGang simply asks a
	user for this admin info when it does not have it, using this form.
	"""

	username = forms.CharField(label=_("admin username"))
	password = forms.CharField(label=_("admin password"), widget=forms.PasswordInput)
	password_verify = forms.CharField(label=_("confirm password"), widget=forms.PasswordInput)

	def __init__(self, blog, *args, **kwargs):
		"""Create a new form for the given blog

		Arguments:
		blog -- a Blog instance

		"""
		self._blog = blog
		super(AdminLoginInfoForm, self).__init__(*args, **kwargs)

	def clean(self):
		"""Verify that the information provided is actually the admin info."""

		data = self.cleaned_data

		# Verify that the passwords match
		if data.get('password') != data.get('password_verify'):
			raise forms.ValidationError(_("The admin passwords must match."))

		# Verify that the information provided is a valid admin login
		username = data.get('username')
		password = data.get('password')
		if username and password:
			if not self._blog.is_admin_login(username, password):
				raise forms.ValidationError(_("The admin username and password provided are not valid."))

		return data

	def update_admin_info(self):
		"""Update the admin username and password.

		This must be called after calling `is_valid()` to avoid errors.
		"""
		self._blog.admin_user = self.cleaned_data['username']
		self._blog.admin_password = self.cleaned_data['password']
		self._blog.save()
