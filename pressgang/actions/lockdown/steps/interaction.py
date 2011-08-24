
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.lockdown.steps import LockdownStep
from pressgang.actions.lockdown.exceptions import LockdownError
from pressgang.actions.options.utils import sitewide_activate_plugin
from pressgang.utils.templates import get_template_dir

import os
import shutil

class Step(LockdownStep):

	name = _("Interactivity restrictions")

	# The name of the directory of the blog being locked down that holds the plugins,
	# relative to the per-blog plugins directory
	_WP_PLUGINS_DIR = "pressgang_lockdown"

	def execute(self, blog, lockdown):
		"""Disable most interactive features of the blog."""

		# Get the source and destination directories for the plugins
		dest_dir = os.path.join(blog.plugins_path, self._WP_PLUGINS_DIR)
		source_dir = get_template_dir('pressgang/lockdown/plugins')
		if not source_dir:
			raise LockdownError(_("Unable to find the lockdown plugins in any of the template directories."))

		# Create a sane baseline by removing old plugins
		self.start(_("Removing old plugins."))
		if os.path.isdir(dest_dir):
			try:
				shutil.rmtree(dest_dir)
			except OSError, e:
				raise LockdownError(_("Unable to remove the old plugins from %(path)s.") % {'path': dest_dir}, e)
		self.complete(_("Old plugins removed."))

		# Only proceed if we're locking down the blog
		if lockdown.locking:

			# Copy the plugins directory to the blog
			self.start(_("Copying plugins."))
			try:
				shutil.copytree(source_dir, dest_dir)
			except OSError, e:
				raise LockdownError(_("Unable to copy the plugins from %(from)s to %(to)s.") % {'from': source_dir, 'to': dest_dir}, e)
			self.complete(_("Plugins copied."))

			# Activate each plugin on the blog
			for plugin in os.listdir(source_dir):
				self.start(_("Activating plugin %(plugin)s.") % {'plugin': plugin})
				sitewide_activate_plugin(os.path.join(self._WP_PLUGINS_DIR, plugin), blog)
				self.complete(_("Plugin %(plugin)s activated.") % {'plugin': plugin})
