
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.revert.steps import RevertStep
from pressgang.actions.revert.exceptions import ReversionError
from pressgang.core.models import VersionSnapshot

class Step(RevertStep):

	name = _("Version snapshot")

	def execute(self, blog, action):
		"""Take a blog version snapshot.

		Note that this is most often used as the first step of any action,
		so the action passed will vary in type, but will always be descended
		from the basic Action class.

		Since any Action class has a public member variable `record`, which
		can have a version snapshot linked to it as a backup, this step creates
		that backup in a way that displays feedback to the user.
		"""

		# Create the version snapshot container, which will allow us to take snapshots
		try:
			snapshot = VersionSnapshot(blog=blog, wp_version=blog.version,
				reason=_("Backup before performing %(action)s action.") % {'action': action.display_name})
			snapshot.save()
			snapshot.prepare_for_snapshot()
		except Exception, e:
			if snapshot:
				snapshot.delete()
			raise ReversionError(_("Unable to create version snapshot container."), e)

		# Take a snapshot of the database
		self.start(_("Exporting database."))
		try:
			snapshot.take_db_snapshot()
		except Exception, e:
			raise ReversionError(_("Unable to export database."), e)
		self.complete(_("Database exported."))

		# Take a snapshot of the WordPress files
		self.start(_("Copying blog files."))
		try:
			snapshot.take_blog_snapshot()
		except Exception, e:
			raise ReversionError(_("Unable to copy blog files."), e)
		self.complete(_("Blog files copied."))

		# Take a snapshot of the Apache config files
		self.start(_("Copying Apache configuration files."))
		try:
			snapshot.take_apache_snapshot()
		except Exception, e:
			raise ReversionError(_("Unable to copy Apache configuration files."), e)
		self.complete(_("Apache configuration files copied."))

		# Once the snapshot is created, associate it with the action's record
		self.start(_("Marking snapshot as backup for this action."))
		action.record.backup = snapshot
		action.record.save()
		self.complete(_("Snapshot marked as backup for this action."))
