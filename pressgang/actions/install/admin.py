
from django.contrib import admin

from pressgang.actions.install.models import InstallationRecord

class InstallationRecordAdmin(admin.ModelAdmin):

	list_display = ('blog_name', 'blog_path', 'started', 'ended', 'succeeded')
	ordering = ('ended',)

admin.site.register(InstallationRecord, InstallationRecordAdmin)
