
from django.db import models
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.models import ActionRecord
from pressgang.core.models import Blog

class LockdownRecord(ActionRecord):
	"""A record of a blog being placed into or taken out of lockdown."""

	class Meta:
		app_label = "pressgang"
		verbose_name = _("lockdown record")
		verbose_name_plural = _("lockdown records")

class LockdownStatusManager(models.Manager):
	"""Custom manager for the LockdownStatus model."""

	def is_blog_locked(self, blog):
		"""Determine whether or not the given blog is in lockdown mode.

		Arguments:
		blog -- a Blog instance

		Returns: a boolean of whether the blog is locked down

		"""
		try:
			status = self.get(blog=blog)
		except LockdownStatus.DoesNotExist:
			return False
		else:
			return status.is_locked

	def update_status(self, blog, is_locked=False):
		"""Update a lockdown status record.

		Arguments:
		blog -- a Blog instance
		is_locked -- a boolean of whether or not the blog is locked

		"""
		try:
			status = self.get(blog=blog)
		except LockdownStatus.DoesNotExist:
			status = self.create(blog=blog, is_locked=is_locked)
		else:
			status.is_locked=is_locked
			status.save()

class LockdownStatus(models.Model):
	"""A record of which blogs are locked down."""

	objects = LockdownStatusManager()

	blog      = models.ForeignKey(Blog, verbose_name=_("blog"))
	is_locked = models.BooleanField(verbose_name=_("is locked down"))

	class Meta:
		app_label = "pressgang"
		verbose_name = _("lockdown status")
		verbose_name_plural = _("lockdown statuses")

	def __unicode__(self):
		return self.blog.title
