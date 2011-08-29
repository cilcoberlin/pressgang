
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.steps import InstallationStep
from pressgang.actions.install.exceptions import InstallationError

import os
import shutil
import tempfile
import urllib
import zipfile

class Step(InstallationStep):

	name = _("Core WordPress files")

	def execute(self, blog, installer):
		"""Copies core WordPress source files to the blog's directory."""

		# Check for installation path conflicts
		if os.path.isdir(blog.path):
			raise InstallationError(_("The blog slug that you have chosen would create a conflict with the directory %(dir)s.  Please use a different slug.") % {'dir': blog.path})
		if os.path.normpath(blog.path) == os.path.normpath(os.path.join(blog.path, "..")):
			raise InstallationError(_("You cannot install blogs in the root directory of the server.  Please use a different installer."))

		# Download the source archive
		self.start(_("Downloading WordPress source archive for version %(version)s.") % {'version': blog.version.full})
		download_dir = tempfile.mkdtemp()
		source_archive = os.path.join(download_dir, "wp-source.zip")
		try:
			urllib.urlretrieve(blog.version.download_url, source_archive)
		except IOError, e:
			raise InstallationError(_("The source archive for WordPress %(version)s could not be downloaded from %(url)s.") % {'version': blog.version.full, 'url': blog.version.download_url}, e)
		self.complete(_("WordPress source archive downloaded."))

		# If it was downloaded, extract its contents to a temporary directory
		self.start(_("Extracting WordPress source files."))
		source_files = zipfile.ZipFile(source_archive, 'r')
		source_dirs = [source_file for source_file in source_files.namelist() if source_file.endswith(os.path.sep)]
		for source_dir in source_dirs:
			new_dir = os.path.join(download_dir, source_dir)
			try:
				os.mkdir(new_dir)
			except OSError, e:
				raise InstallationError(_("Unable to extract the %(dir)s directory from the WordPress source archive.") % {'dir': new_dir}, e)
		for filename in source_files.namelist():
			if not filename.endswith(os.path.sep):
				new_file = open(os.path.join(download_dir, filename), 'wb')
				new_file.write(source_files.read(filename))
				new_file.close()
		source_files.close()
		self.complete(_("WordPress source files extracted."))

		# Move the source files to the blog's installation path
		self.start(_("Installing WordPress source files."))
		wp_source_dir = os.path.join(download_dir, "wordpress")
		blog_parent_dir = os.path.normpath(os.path.join(blog.path, os.pardir))
		if not os.path.isdir(blog_parent_dir):
			try:
				os.makedirs(blog_parent_dir, 0755)
			except OSError, e:
				raise InstallationError(_("Unable to create the parent directories for the blog at %(blog_dir)s.") % {'blog_dir': blog.path}, e)
		try:
			os.rename(wp_source_dir, blog.path)
		except OSError, e:
			raise InstallationError(_("Unable to copy WordPress files to the blog's directory in %(blog_dir)s.") % {'blog_dir': blog.path}, e)
		self.complete(_("WordPress source files installed."))
		shutil.rmtree(download_dir)
