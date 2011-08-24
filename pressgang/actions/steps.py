
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _

from pressgang.core.exceptions import PressGangConfigurationError, PressGangError

import inspect

def get_step(module):
	"""Returns an instance of an ActionStep descendant with the given ID.

	The id provided will be a string of the full module path to a model
	containing a class named Step descended from the ActionStep class.  If a
	step cannot be found, a PressGang error is raised.

	Arguments:
	module -- the string of the module containing steps for the action
	id -- the ID of a step

	Returns: an ActionStep instance or None if the step is invalid

	"""
	try:
		step_module = import_module(module)
	except ImportError:
		raise PressGangError(_("The module %(module)s is not a valid module.") % {'module': id})
	else:
		try:
			return step_module.Step()
		except AttributeError:
			raise PressGangError(_("The module %(module)s must define a class %(child)s that inherits from %(parent)s.") % {'module': id, 'child': 'Step', 'parent': 'ActionStep'})

class ActionStep(object):
	"""Base class for a step in an action performed on a blog."""

	# The name of the step
	name = None

	def start(self, message):
		"""Log the beginning of an action."""
		self._logger.start_action(self.name, message)

	def complete(self, message):
		"""Log the completion of an action."""
		self._logger.end_action(message)

	def run(self, blog, action, record):
		"""Perform the step.

		This method differs from `execute` in that this should not be overridden
		by a descendant class, as it is a wrapper to handle global step logic.

		Arguments:
		blog -- a Blog instance of the blog on which the action is being performed
		action -- an Action-descended instance of the action being performed
		record -- an ActionRecord instance for tracking the action's progress

		"""

		if not self.name:
			step_path = inspect.getmodule(self).__name__
			raise PressGangConfigurationError(_("The step at %(path)s must provide a name by defining a value for name.") % {'path': step_path})

		# Run the descendant-provided code to execute the step
		self._logger = record.log
		self.execute(blog, action)

	def execute(self, blog, action):
		"""Perform the actions needed to make the step happen.

		This method must be overridden by a descendant class.

		Arguments
		blog -- a Blog instance of the blog on which the action is being done
		action -- an Action-descended instance of the action being performed

		"""
		raise NotImplementedError
