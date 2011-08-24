
from django.db.models import signals

import pressgang.models as pressgang_app
from pressgang.management.commands.syncblogs import Command as SyncBlogsCommand

def sync_blogs(app, created_models, verbosity, **kwargs):
	"""Sync the blog list whenever the database is synced."""
	syncblogs = SyncBlogsCommand()
	syncblogs.execute()

signals.post_syncdb.connect(sync_blogs, sender=pressgang_app)
