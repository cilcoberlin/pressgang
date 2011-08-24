
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

		# Create the file and store a writable reference to it
		plugin_name = "pressgang_%s.php" % "".join([random.choice(string.ascii_lowercase) for i in xrange(0, 10)])
		self._plugin_path = os.path.join(base_dir, plugin_name)

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
		os.remove(self._plugin_path)
