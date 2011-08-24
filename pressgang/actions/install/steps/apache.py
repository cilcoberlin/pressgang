
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.steps import InstallationStep
from pressgang.actions.install.exceptions import InstallationError
from pressgang.utils.apache import reload_apache

class Step(InstallationStep):

	name = _("Apache configuration")

	def execute(self, blog, installer):
		"""Configures Apache to be able to serve the blog."""

		# Create a configuration file for the blog that will be loaded by Apache
		self.start(_("Creating Apache configuration file."))
		try:
			blog.create_standalone_apache_conf()
		except Exception, e:
			raise InstallationError(_("An Apache configuration file for the blog could not be created."), e)
		self.complete(_("Apache configuration file created."))

		# Reload the Apache configuration files
		self.start(_("Gracefully restarting Apache."))
		try:
			reload_apache()
		except OSError, e:
			raise InstallationError(_("Apache could not be restarted."), e)
		self.complete(_("Apache gracefully reloaded."))
