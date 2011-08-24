
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.encoding import force_unicode
import django.utils.simplejson as json

from functools import wraps

class AjaxError(Exception):
	"""A custom error thrown when something goes wrong in an Ajax view."""
	pass

def ajax_view(view_function):
	"""A decorator that converts a dict returned by a decorated as a JSON response."""

	def wrapper(request, *args, **kwargs):

		#  Get our view response and handle exceptions if we're debugging
		Response = HttpResponse
		view_success = True
		error_message = u""
		try:
			response_data = view_function(request, *args, **kwargs)
		except AjaxError, e:
			view_success = False
			error_message = force_unicode(e.message)
			response_data = {'message': error_message.capitalize()}
			Response = HttpResponseBadRequest
		except Exception, e:
			raise e

		#  If the return type of the view is a standard HTTP response, render that
		if hasattr(response_data, 'status_code'):
			return response_data

		#  Or make it a JSON response, adding in our predetermined success value
		#  and a possible error text obtained from a caught AjaxError
		else:
			response_data['success'] = view_success
			json_response = Response(mimetype="application/json")
			json.dump(response_data, fp=json_response)
			return json_response

	return wraps(view_function)(wrapper)
