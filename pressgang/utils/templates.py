
from django.conf import settings

import os

def get_template_dir(relative_path):
	"""Get the absolute path to the directory from which the given relative path is served.

	Arguments:
	relative_path -- the relative path to a template directory or file

	Returns: the absolute path to the resource's directory

	"""
	full_path = None
	for template_dir in settings.TEMPLATE_DIRS:
		temp_path = os.path.join(template_dir, relative_path)
		if os.path.exists(temp_path):
			full_path = temp_path
			break
	if full_path:
		if os.path.isfile(full_path):
			full_path = os.path.dirname(full_path)
	return full_path

