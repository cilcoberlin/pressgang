from django.conf.urls.defaults import include, patterns, url

blog_patterns = patterns('pressgang.actions.install.addblogs.views',
	url(r'^options/$', 'add_blogs_options', name="add-blogs-options"),
)

blog_patterns += patterns('pressgang.actions.views',
	url(r'^execute/$', 'execute_action', name="add-blogs")
)

urlpatterns = patterns('',
	(r'^(?P<blog_id>\d+)/', include(blog_patterns)),
)
