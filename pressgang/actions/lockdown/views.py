
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404

from pressgang.accounts.decorators import can_manage_blogs
from pressgang.actions import store_action
from pressgang.actions.lockdown import LockdownAction
from pressgang.core.decorators import admin_info_required
from pressgang.core.models import Blog
from pressgang.utils.pages import Page

@can_manage_blogs
@admin_info_required
def confirm_lockdown(request, blog_id=None, lock=None):
	"""Allows the user to confirm whether or not they wish to lock down the blog."""

	# Prevent an amibugous or redundant lockdown
	if lock is None:
		raise Http404
	blog = get_object_or_404(Blog, pk=blog_id)
	if blog.is_locked == lock:
		raise Http404

	page = Page(request)
	page.add_render_args({
		'blog': blog,
		'lock': lock
	})
	return page.render('pressgang/lockdown/confirm.html')

@can_manage_blogs
@admin_info_required
def create_action(request, blog_id=None, lock=None):
	"""Creates the appropriate type of lockdown action for the user."""

	# Prevent an amibugous or redundant lockdown
	if lock is None:
		raise Http404
	blog = get_object_or_404(Blog, pk=blog_id)
	if blog.is_locked == lock:
		raise Http404

	# Create the proper type of lockdown action and go to the execution page
	store_action(request, LockdownAction(blog, lock=lock))
	lock_view = 'lock-blog' if lock else 'unlock-blog'
	return HttpResponseRedirect(reverse(lock_view, kwargs={'blog_id': blog_id}))



