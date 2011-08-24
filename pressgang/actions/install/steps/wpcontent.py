
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.steps import InstallationStep
from pressgang.actions.install.exceptions import InstallationError
from pressgang.core.models import Blog

import os
import shutil

class Step(InstallationStep):

	name = _("Custom themes and plugins")

	def execute(self, blog, installer):
		"""Installs custom wp-content from the installer to the blog."""

		# Copy any plugins, MU plugins or themes associated with the current installer
		for content_dir in Blog.WP_CONTENT_DIRS:
			self.start(_("Copying custom WordPress %(dir)s content.") % {'dir': content_dir})
			content_from = os.path.join(installer.path, content_dir)
			if os.path.isdir(content_from):
				content_to = os.path.join(blog.wp_content_path, content_dir)
				if not os.path.isdir(content_to):
					try:
						os.mkdir(content_to)
					except OSError, e:
						raise InstallationError(_("The WordPress content directory at %(path)s could not be created.") % {'path': content_to }, e)
				for content in os.listdir(content_from):
					source = os.path.join(content_from, content)
					destination = os.path.join(content_to, content)
					if os.path.isfile(source):
						try:
							shutil.copyfile(source, destination)
						except (IOError, shutil.Error), e:
							raise InstallationError(_("The WordPress content file at %(source)s could not be copied to %(destination)s.") % {'source': source, 'destination': destination}, e)
					elif os.path.isdir(source):
						if not os.path.isdir(destination):
							try:
								shutil.copytree(source, destination)
							except shutil.Error, e:
								raise InstallationError(_("The WordPress content directory at %(source)s could not be copied to %(destination)s.") % {'source': source, 'destination': destination}, e)
			self.complete(_("Custom WordPress %(dir)s content copied.") % {'dir': content_dir})
