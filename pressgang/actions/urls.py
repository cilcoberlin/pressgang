from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pressgang.actions.views',
	url(r'^begin/$', 'begin_action', name="begin-action"),
	url(r'^progress/$', 'action_progress', name="action-progress")
)
