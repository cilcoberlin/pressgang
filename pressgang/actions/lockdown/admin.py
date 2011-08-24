
from django.contrib import admin

from pressgang.actions.lockdown.models import LockdownRecord

class LockdownRecordAdmin(admin.ModelAdmin):

	list_display = ('blog_name', 'blog_path', 'started', 'ended', 'succeeded')
	ordering = ('ended',)

admin.site.register(LockdownRecord, LockdownRecordAdmin)
