from django.conf.urls.defaults import *

revert_patterns = patterns('pressgang.actions.revert.views',
	url(r'^version/$', 'reversion_options', name="reversion-options"),
)

revert_patterns += patterns('pressgang.actions.views',
	url(r'^execute/$', 'execute_action', name="revert-blog")
)

urlpatterns = patterns('',
	(r'^(?P<blog_id>\d+)/', include(revert_patterns)),
)
