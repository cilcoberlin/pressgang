
from django import forms
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install import find_installers, load_installer
from pressgang.core.exceptions import PressGangConfigurationError

class InstallerSelectField(forms.ChoiceField):
	"""A field that allows a user to select an installer."""

	def __init__(self, *args, **kwargs):
		"""Use a list of installers as the data set."""

		if 'choices' not in kwargs:
			kwargs['choices'] = find_installers()
		super(InstallerSelectField, self).__init__(*args, **kwargs)

	def clean(self, value):
		"""Convert the user selection to an Installer-derived class."""

		installer = None

		# Try to load the installer if the user has selected a non-empty value.
		# If the installer fails to load, a PressGangConfigurationError is raised,
		# and this can be caught to in turn throw a validation error to the user.
		if value:
			try:
				installer = load_installer(value)
			except PressGangConfigurationError:
				raise forms.ValidationError(_("This package does not appear to be a valid installer.  Please select another installer."))
		return installer
