from django.conf.urls.defaults import *

urlpatterns = patterns('pressgang.actions.manage.views',
	url(r'^/?$', 'list_blogs', name="list-blogs"),
)
