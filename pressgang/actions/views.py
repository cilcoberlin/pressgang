
from django.http import Http404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from pressgang.accounts.decorators import can_manage_blogs
from pressgang.actions import clear_action, retrieve_action
from pressgang.utils.ajax import ajax_view, AjaxError
from pressgang.utils.pages import Page

@can_manage_blogs
def execute_action(request, **kwargs):
	"""A page that executes an action.

	For this view to be called, there must be a cached Action-descended instance
	available as a session variable available through the 'current_action' key.
	"""

	action = retrieve_action(request)
	if not action:
		raise Http404

	page = Page(request)
	page.add_render_args({
		'action': action,
		'blog':   action.blog
	})
	return page.render(action.execute_template)

@can_manage_blogs
@ajax_view
def begin_action(request):
	"""Begins executing the current cached action."""

	action = retrieve_action(request)
	if not action:
		raise AjaxError(_("No action could be found in the session."))

	# Execute the action asynchronously
	try:
		action.execute_async()
	except Exception, e:
		raise AjaxError(_("Unable to start the action %(action)s: %(error)s") % {'error': e, 'action': action.display_name})

	return {}

@can_manage_blogs
@ajax_view
def action_progress(request):
	"""Fetches an update on the progress of an action.

	This is used to display feedback to the user on the action, as this
	view is called in a loop while the action is being performed.
	"""

	action = retrieve_action(request)
	if not action:
		raise AjaxError(_("No action could be found in the session"))

	# Refresh the action's record to avoid using a stale record
	try:
		record = action.Record.objects.get(pk=action.record.pk)
	except action.Record.DoesNotExist:
		raise AjaxError(_("No action record could be found."))

	# Clear the cached action if it has been completed
	if record.is_ended:
		clear_action(request)

	return {
		'ended': record.is_ended,
		'failed': record.is_failed,
		'markup': {
			'log': render_to_string(action.log_template, {
				'action': action,
				'blog': action.blog,
				'log': record.log,
				'record': record,
				'succeeded': record.succeeded
			})
		}
	}
