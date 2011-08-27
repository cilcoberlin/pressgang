
from django.contrib import admin

from pressgang.actions.install.addblogs.models import BlogAdditionRecord

class BlogAdditionRecordAdmin(admin.ModelAdmin):

	list_display = ('blog_name', 'blog_path', 'started', 'ended', 'succeeded')
	ordering = ('ended',)

admin.site.register(BlogAdditionRecord, BlogAdditionRecordAdmin)
