from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pressgang.core.views',
	url(r'^/?$', 'pressgang_home', name='home'),
	url(r'^admin-info/(?P<blog_id>\d+)/$', 'get_admin_info', name="get-admin-info")
)
