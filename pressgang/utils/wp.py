
import os
import random
import string

class TemporaryPlugin(object):
	"""A temporary plugin used by PressGang to make changes to a blog."""

	def __init__(self, base_dir):
		"""Create a new temporary plugin file.

		Arguments:
		base_dir -- the full path to the directory in which the file should be created

		"""

		# Create the file and store its path
		conflicts = True
		while conflicts:
			self._plugin_path = os.path.join(base_dir, self._generate_file_name())
			if not os.path.isfile(self._plugin_path):
				open(self._plugin_path, 'w').close()
				conflicts = False

	def _generate_file_name(self):
		"""Create a random file name for a plugin.

		Returns: a string of the full path to a plugin file name

		"""
		return "pressgang_%s.php" % "".join([random.choice(string.ascii_lowercase) for i in xrange(0, 10)])

	def write(self, data):
		"""Write data to the plugin file.

		Arguments:
		data -- a string of data to write to the file

		"""
		file = open(self._plugin_path, 'w')
		file.write(data)
		file.close()

	def remove(self):
		"""Removes the plugin file."""
		if os.path.isfile(self._plugin_path):
			os.remove(self._plugin_path)
