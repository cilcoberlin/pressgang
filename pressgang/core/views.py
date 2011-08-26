
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from pressgang.accounts.decorators import can_manage_blogs
from pressgang.accounts.models import PressGangUser
from pressgang.core.forms import AdminLoginInfoForm
from pressgang.core.models import Blog
from pressgang.utils.pages import Page

# The name of the GET parameter defining a page to redirect to
NEXT_PAGE_PARAM = "next"

def handle_404(request):
	"""Handle a page-not-found error."""
	page = Page(request)
	return page.render('pressgang/core/error404.html')

def handle_500(request):
	"""Handle a server error."""
	page = Page(request)
	return page.render('pressgang/core/error500.html')

@login_required
def pressgang_home(request):
	"""Base page for PressGang that redirects an authenticated user."""

	# Figure out a redirection URL based on the user's permissions
	user = PressGangUser.objects.get(pk=request.user.pk)
	redirect_to = None
	if user.can_manage_blogs() or user.can_view_blogs():
		redirect_to = reverse("pressgang:list-blogs")
	elif user.can_install_blogs():
		redirect_to = reverse("pressgang:install-blog")

	# Redirect the user or prevent them access if they have no PressGang permissions
	if not redirect_to:
		return HttpResponseRedirect(reverse('pressgang:access-denied'))
	else:
		return HttpResponseRedirect(redirect_to)

@can_manage_blogs
def get_admin_info(request, blog_id=None):
	"""Allows the user to provide admin login information for a blog.

	This is the view that a view decorated with the admin_info_required decorator
	redirects to if no admin login information can be found for a blog in
	the decorated view.

	Once the admin information is provided and verified, the user is returned
	to the page that they were previously tring to access.
	"""

	blog = get_object_or_404(Blog, pk=blog_id)
	next_page = request.GET.get(NEXT_PAGE_PARAM) or request.POST.get(NEXT_PAGE_PARAM)

	# Update the admin info and send the user to the page they originally wanted
	# to access, provided that the info provided is correct
	if request.POST:
		admin_form = AdminLoginInfoForm(blog, request.POST)
		if admin_form.is_valid():
			admin_form.update_admin_info()
			if not next_page:
				next_page = reverse('pressgang:list-blogs')
			return HttpResponseRedirect(next_page)
	else:
		admin_form = AdminLoginInfoForm(blog)

	page = Page(request)
	page.add_render_args({
		'admin_form': admin_form,
		'blog': blog,
		'next_page': next_page,
		'next_param': NEXT_PAGE_PARAM
	})
	return page.render('pressgang/core/admin_info.html')
