from django.conf.urls.defaults import patterns, include, url

pressgang_patterns = patterns('',
	(r'^', include('pressgang.core.urls')),
	(r'^accounts/', include('pressgang.accounts.urls')),
	(r'^actions/', include('pressgang.actions.urls')),
	(r'^addblogs/', include('pressgang.actions.install.addblogs.urls')),
	(r'^install/', include('pressgang.actions.install.urls')),
	(r'^lockdown/', include('pressgang.actions.lockdown.urls')),
	(r'^manage/', include('pressgang.actions.manage.urls')),
	(r'^revert/', include('pressgang.actions.revert.urls')),

	url(r'^jsi18n/', 'django.views.i18n.javascript_catalog', {'packages': 'pressgang'}, "jsi18n-catalog")
)

urlpatterns = patterns('',
	(r'^', include(pressgang_patterns, namespace='pressgang'))
)
