
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.steps import InstallationStep
from pressgang.actions.install.exceptions import InstallationError

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
