
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from pressgang.core.exceptions import PressGangConfigurationError
from pressgang.core.models import Blog
from pressgang.core.views import NEXT_PAGE_PARAM

from functools import wraps

def admin_info_required(view_function):
	"""
	A decorator that should be applied to any view that performs an operation
	on a single blog that requires a valid admin username and password.

	The decorated view must receive a `blog_id` kwarg for this decorator to work.
	If the view does not provide this, a PressGangConfigurationError is raised.
	"""

	def wrapper(request, *args, **kwargs):

		# Verify that the decorator is placed on a view that uses a blog ID
		if _BLOG_ID_KWARG not in kwargs:
			raise PressGangConfigurationError(_("Any view decorated with %(decorator)s must receive a blog ID via the kwarg %(kwarg)s") % {'decorator': 'admin_info_required', 'kwarg': _BLOG_ID_KWARG})

		# If the blog referenced can't be found, just return the view's response,
		# so that it can produce a 404 if it wishes to
		response = view_function(request, *args, **kwargs)
		try:
			blog = Blog.objects.get(pk=kwargs[_BLOG_ID_KWARG])
		except Blog.DoesNotExist:
			return response

		# If the blog does not have admin information defined, redirect to a
		# page that asks the user for this information
		if not blog.admin_user or not blog.admin_password:
			return HttpResponseRedirect("%(url)s?%(param)s=%(next)s" % {
				'url': reverse('get-admin-info', kwargs={'blog_id': blog.pk}),
				'param': NEXT_PAGE_PARAM,
				'next': urlquote(request.get_full_path())
			})
		return response

	return wraps(view_function)(wrapper)
_BLOG_ID_KWARG = "blog_id"

