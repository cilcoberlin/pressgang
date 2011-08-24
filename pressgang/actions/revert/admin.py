
from django.contrib import admin

from pressgang.actions.revert.models import ReversionRecord

class ReversionRecordAdmin(admin.ModelAdmin):

	list_display = ('blog_name', 'blog_path', 'started', 'ended', 'succeeded')
	ordering = ('ended',)

admin.site.register(ReversionRecord, ReversionRecordAdmin)
