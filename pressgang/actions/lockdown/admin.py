
from django.contrib import admin

from pressgang.actions.lockdown.models import LockdownRecord, LockdownStatus

class LockdownRecordAdmin(admin.ModelAdmin):

	list_display = ('blog_name', 'blog_path', 'started', 'ended', 'succeeded')
	ordering = ('ended',)

class LockdownStatusAdmin(admin.ModelAdmin):

	list_display = ('blog', 'is_locked')
	ordering = ('blog__path',)

admin.site.register(LockdownRecord, LockdownRecordAdmin)
admin.site.register(LockdownStatus, LockdownStatusAdmin)
