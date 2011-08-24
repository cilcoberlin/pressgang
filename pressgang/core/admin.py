
from django.contrib import admin

from pressgang.core.models import Blog, VersionSnapshot, WordPressVersion

class BlogAdmin(admin.ModelAdmin):

	list_display = ('path', 'title', 'version', 'created', 'is_locked')
	ordering = ('path',)

class VersionSnapshotAdmin(admin.ModelAdmin):

	list_display = ('blog', 'wp_version', 'created', 'reason')
	ordering = ('created',)

class WordPressVersionAdmin(admin.ModelAdmin):

	list_display = ('full', 'major', 'minor', 'is_multi')
	ordering = ('full',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(VersionSnapshot, VersionSnapshotAdmin)
admin.site.register(WordPressVersion, WordPressVersionAdmin)
