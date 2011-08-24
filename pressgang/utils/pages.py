
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

class Page(object):
	"""
	A base class representing a page that can be displayed to a user in a Django
	app that can encapsulate functionality to be used across similar views.

	This class is used in views as follows:

	>>> page = Page(request)
	>>> page.add_render_args({'your_arg': 'arg_val'})
	>>> return page.render('path_to/your_template.html')

	"""

	def __init__(self, request):
		"""Requires the Request instance as its first argument."""
		self.request = request
		self._render_args = {}

	def add_render_args(self, render_args):
		"""Add arguments that are passed to the render_to_response function"""
		self._render_args.update(render_args)

	def render(self, template_name, to_string=False):
		"""
		Return markup for the page, using the assembled rendering arguments and
		the template path provided in `template_name`.

		If the `to_string` keyword argument is False, the page is returned as an
		HttpResponse instance. If it is True, it is returned as a string.
		"""

		#  Return either an HTTP response object or a simple string, based on
		#  the requested rendering type
		render_function = render_to_string if to_string else render_to_response
		return render_function(template_name,
							   self._render_args,
							   context_instance=RequestContext(self.request))
