from django.conf.urls.defaults import *

urlpatterns = patterns('pressgang.actions.install.views',
	url(r'^/?$', 'install_options', name="install-options"),
)

urlpatterns += patterns('pressgang.actions.views',
	url(r'^install/(?P<slug>[0-9a-zA-Z_-]+)/$', 'execute_action', name="install-blog"),
)
