
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404

from pressgang.accounts.decorators import can_manage_blogs
from pressgang.actions import store_action
from pressgang.actions.install.addblogs import AddBlogsAction
from pressgang.actions.install.addblogs.forms import BlogAdditionForm
from pressgang.core.decorators import admin_info_required
from pressgang.core.models import Blog
from pressgang.utils.pages import Page

@can_manage_blogs
@admin_info_required
def add_blogs_options(request, blog_id=None):
	"""Allows the user to specify options for adding child blogs to a blog."""

	# If the blog cannot support child blogs, raise a 404
	blog = get_object_or_404(Blog, pk=blog_id)
	if not blog.version.is_multi:
		raise Http404

	# If valid options were provided, begin adding the child blogs
	if request.POST:
		add_form = BlogAdditionForm(request.POST)
		if add_form.is_valid():
			store_action(request, AddBlogsAction(blog,
				users=add_form.cleaned_data['users'],
				blog_type=add_form.cleaned_data['blog_type']))
			return HttpResponseRedirect(reverse("pressgang:add-blogs", kwargs={'blog_id': blog.pk}))
	else:
		add_form = BlogAdditionForm()

	page = Page(request)
	page.add_render_args({
		'blog': blog,
		'add_form': add_form
	})
	return page.render('pressgang/addblogs/options.html')
