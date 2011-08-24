
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404

from pressgang.accounts.decorators import can_manage_blogs
from pressgang.actions import store_action
from pressgang.actions.revert import RevertAction
from pressgang.actions.revert.forms import ReversionForm
from pressgang.core.decorators import admin_info_required
from pressgang.core.models import Blog
from pressgang.utils.pages import Page

@can_manage_blogs
@admin_info_required
def reversion_options(request, blog_id=None):
	"""Allows the user to select which blog version to revert to."""

	# If the blog has no version snapshots, raise a 404
	blog = get_object_or_404(Blog, pk=blog_id)
	if not blog.has_version_snapshots:
		raise Http404

	# If a valid version was selected, begin the reversion process
	if request.POST:
		revert_form = ReversionForm(blog, request.POST)
		if revert_form.is_valid():
			store_action(request, RevertAction(blog, snapshot=revert_form.cleaned_data['snapshot']))
			return HttpResponseRedirect(reverse("revert-blog", kwargs={'blog_id': blog.pk}))
	else:
		revert_form = ReversionForm(blog)

	page = Page(request)
	page.add_render_args({
		'blog': blog,
		'revert_form': revert_form
	})
	return page.render('pressgang/revert/options.html')
