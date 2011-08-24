
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.revert.steps import RevertStep
from pressgang.actions.revert.exceptions import ReversionError

class Step(RevertStep):

	name = _("Reversion")

	def execute(self, blog, reversion):
		"""Revert the blog to a previous version snapshot."""

		snapshot = reversion.snapshot

		# Restore the database
		self.start(_("Restoring database."))
		try:
			snapshot.revert_db()
		except Exception, e:
			raise ReversionError(_("Unable to restore database."), e)
		self.complete(_("Database restored."))

		# Restore the WordPress files
		self.start(_("Restoring blog files."))
		try:
			snapshot.revert_blog_files()
		except Exception, e:
			raise ReversionError(_("Unable to restore blog files."), e)
		self.complete(_("Blog files restored."))

		# Restore the Apache config files
		self.start(_("Restoring Apache configuration files."))
		try:
			snapshot.revert_apache_files()
		except Exception, e:
			raise ReversionError(_("Unable to restore Apache files."), e)
		self.complete(_("Apache configuration files restoring."))
