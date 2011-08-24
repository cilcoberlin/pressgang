
from pressgang.accounts.decorators import can_view_blogs
from pressgang.core.models import Blog, WordPressVersion
from pressgang.utils.pages import Page

@can_view_blogs
def list_blogs(request):
	"""Displays all blogs on the site to a user."""
	page = Page(request)
	page.add_render_args({
		'blogs': Blog.objects.list_by_path(),
		'current_version': WordPressVersion.objects.current_version()
	})
	return page.render('pressgang/manage/list.html')
