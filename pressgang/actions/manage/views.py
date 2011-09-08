
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from pressgang.accounts.decorators import can_view_blogs
from pressgang.core.models import Blog, WordPressVersion
from pressgang.utils.pages import Page

@can_view_blogs
def list_blogs(request):
	"""Displays all blogs on the site to a user."""

	# Get our sync result if we have one
	try:
		synced = request.session['synced']
	except KeyError:
		synced = False
	else:
		del request.session['synced']

	page = Page(request)
	page.add_render_args({
		'blogs': Blog.objects.list_by_date(),
		'current_version': WordPressVersion.objects.current_version(),
		'synced': synced
	})
	return page.render('pressgang/manage/list.html')

@can_view_blogs
def sync_blogs(request):
	"""Syncs the list of blogs installed on the server with the database."""
	Blog.objects.sync_blogs()
	request.session['synced'] = True
	return HttpResponseRedirect(reverse("pressgang:list-blogs"))
