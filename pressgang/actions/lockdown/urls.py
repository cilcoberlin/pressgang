from django.conf.urls.defaults import *

lock_patterns = patterns('pressgang.actions.lockdown.views',
	url(r'^confirm/$', 'confirm_lockdown', {'lock': True}, "confirm-lockdown"),
	url(r'^start$', 'create_action', {'lock': True}, "start-lockdown")
)

lock_patterns += patterns('pressgang.actions.views',
	url(r'^execute/$', 'execute_action', name="lock-blog")
)

unlock_patterns = patterns('pressgang.actions.lockdown.views',
	url(r'^confirm/$', 'confirm_lockdown', {'lock': False}, "confirm-unlock"),
	url(r'^start$', 'create_action', {'lock': False}, "start-unlock"),
)

unlock_patterns += patterns('pressgang.actions.views',
	url(r'^execute/$', 'execute_action', name="unlock-blog"),
)

blog_patterns = patterns('',
	(r'^lock/', include(lock_patterns)),
	(r'^unlock/', include(unlock_patterns))
)

urlpatterns = patterns('',
	(r'^(?P<blog_id>\d+)/', include(blog_patterns)),
)
