
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.exceptions import ActionError
from pressgang.actions.models import ActionRecord
from pressgang.actions.steps import get_step
from pressgang.core.exceptions import PressGangError, PressGangConfigurationError
from pressgang.core.models import VersionSnapshot

import inspect
import threading

# The session key used to store an in-progress action
_ACTION_SESSION_KEY = "current_action"

def store_action(request, action):
	"""Store the given action in the request's session cache.

	Arguments:
	request -- an HTTPRequest instance
	action -- an Action subclass instance

	"""
	request.session[_ACTION_SESSION_KEY] = action

def retrieve_action(request):
	"""Retrieve a cached action from the current session.

	Arguments:
	request -- an HTTPRequest instance

	Returns: the cached Action subclass instance, or None if no action was cached

	"""
	return request.session.get(_ACTION_SESSION_KEY, None)

def clear_action(request):
	"""Clear an action from the session's cache.

	Arguments:
	request -- an HTTPRequest instance

	"""
	try:
		del request.session[_ACTION_SESSION_KEY]
	except KeyError:
		pass

class AsynchronousAction(threading.Thread):
	"""Thread for asynchronously performing an action on a blog."""

	def __init__(self, action):
		"""Create the new thread for the action executer.

		Arguments:
		action -- an Action-descended instance

		"""
		self.action = action
		super(AsynchronousAction, self).__init__()

	def run(self):
		"""Perform the action."""

		# Since this threaded action will only be run through an Ajax call via
		# the web-based interface, which uses Ajax polling to display the logged
		# action events, we ignore any exceptions raised during the action,
		# as they will be handled by the logger.
		try:
			self.action.execute()
		except ActionError, e:
			if settings.DEBUG:
				raise e

class Action(object):
	"""Base class for any action that can be performed on a blog."""

	# The name shown for this action
	display_name = None

	# The template to use for display the action's log
	log_template = "pressgang/actions/record.html"

	# The template to use for displaying the action's execution page
	execute_template = "pressgang/actions/execute.html"

	# The class to use to track the action
	Record = ActionRecord

	# The steps to perform as part of the action
	steps = []

	# Whether or not the action can support version snapshots to revert back to
	supports_reversion = True

	def __init__(self, blog):
		"""Create a new Action instance.

		Arguments:
		blog -- the blog on which the action will be performed

		"""

		# Make sure that the action is properly configured
		self._steps = self.provide_steps() or self.steps
		module_name = inspect.getmodule(self).__name__
		if not self._steps:
			raise PressGangConfigurationError(_("The action %(action)s must provide at least one step via the %(var)s variable.") % {'action': module_name, 'var': 'steps'})

		# Store the blog and create a record to track it
		self.blog = blog
		self.record = self.Record.new_record(self.blog)

	def execute(self):
		"""Performs the actual action of the blog.

		The action is performed by calling a series of steps.  If any of these
		steps encounters an error, it raises an exception descended from
		ActionError, which can then be handled by higher-level code.
		"""

		# If the blog supports version snapshots for reversion, take a snapshot
		# as the first step of the action
		if self.supports_reversion:
			self._steps = ['pressgang.actions.revert.steps.snapshot'] + self._steps

		# Execute each step in sequence, halting on any errors
		for step_id in self._steps:
			try:
				try:
					step = get_step(step_id)
				except PressGangError, e:
					raise ActionError(_("%(step)s is not a valid step ID.") % {'step': step_id}, e)
				else:
					step.run(self.blog, self, self.record)
			except ActionError, e:
				self._handle_error(e)

		# Allow a child action to run its own code on success
		self.on_success(self.blog)

		# End the record of the action
		self.record.finalize(self.blog)

		# Save the blog to make sure that the blog's file structure is in line
		# with its database representation
		self.blog.save()

	def on_error(self, blog, error):
		"""Handle an error that occured during execution.

		Arguments:
		blog -- a Blog instance
		error -- an ActionError-descended instance

		"""
		pass

	def on_success(self, blog):
		"""Handle the successful completion of an action.

		Arguments:
		blog -- a Blog instance

		"""
		pass

	def execute_async(self):
		"""Asynchronously perform the action on the blog in a separate thread.

		This is used to make performing the action through the web interface
		possible to log in pseudo-realtime.
		"""
		AsynchronousAction(self).start()

	def provide_steps(self):
		"""Allows a child action to dynamically provide steps.

		Returns: a list of full paths to step modules

		"""
		return []

	def _handle_error(self, e):
		"""Handle an error that occurs during execution.

		Keyword Arguments:
		e -- an ActionError instance

		"""

		# Allow a child action to handle errors how it wants
		self.on_error(self.blog, e)

		# End the action log
		self.record.abort(e)

		# If a pre-action backup exists, attempt to revert to it
		if self.record.backup:
			self.record.backup.revert()

		# Raise the ActionError to allow higher-level code to handle it, or,
		# if we're debugging, raise the raw Exception
		if settings.DEBUG and e.error_info:
			raise e.error_info
		raise e

