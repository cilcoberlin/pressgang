
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from pressgang.accounts.decorators import can_install_blogs
from pressgang.actions import store_action
from pressgang.actions.install.forms import InstallBlogForm
from pressgang.utils.pages import Page

@can_install_blogs
def install_options(request):
	"""Allows the user to provide options for installing a new blog."""

	if request.POST:
		install_form = InstallBlogForm(request.POST)
		if install_form.is_valid():
			store_action(request, install_form.create_installer())
			return HttpResponseRedirect(reverse('install-blog', kwargs={'slug': install_form.cleaned_data['slug']}))
	else:
		install_form = InstallBlogForm()

	page = Page(request)
	page.add_render_args({
		'install_form': install_form
	})
	return page.render('pressgang/install/options.html')

