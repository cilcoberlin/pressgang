
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from pressgang.core.models import Blog

class Command(BaseCommand):

	help = _("syncs the list of blogs installed on the server")

	def handle(self, *args, **kwargs):
		"""Create a list of blogs installed on the server."""
		Blog.objects.sync_blogs(interactive=True)
