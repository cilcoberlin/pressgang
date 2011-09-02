from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pressgang.actions.manage.views',
	url(r'^/?$', 'list_blogs', name="list-blogs"),
	url(r'^sync-blogs/$', 'sync_blogs', name="sync-blogs"),
)
