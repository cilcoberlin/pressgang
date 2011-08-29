
from django.db import models
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _

from pressgang.core.exceptions import PressGangError
from pressgang.core.models import Blog, VersionSnapshot

import datetime

class ActionRecord(models.Model):
	"""A record of an action performed on a blog."""

	blog      = models.ForeignKey(Blog, null=True, blank=True, verbose_name=_("blog"))
	blog_name = models.CharField(max_length=255, verbose_name=_("blog name"))
	blog_path = models.CharField(max_length=255, verbose_name=_("blog path"))
	started   = models.DateTimeField(auto_now_add=True, verbose_name=_("start timestamp"))
	ended     = models.DateTimeField(null=True, blank=True, verbose_name=_("end timestamp"))
	succeeded = models.BooleanField(default=False, verbose_name=_("succeeded"))
	backup    = models.ForeignKey(VersionSnapshot, null=True, blank=True, verbose_name=_("backup of the blog"))

	class Meta:

		app_label = "pressgang"
		verbose_name = _("action record")
		verbose_name_plural = _("action records")

	def __unicode__(self):
		return _("%(blog)s (%(date)s)") % {'blog': self.blog_name, 'date': self.ended}

	@classmethod
	def new_record(cls, blog):
		"""Create a new record for the given blog.

		Arguments:
		blog -- an instance of a Blog model

		Returns: an instance of an ActionRecord model

		"""

		record = cls(blog_name=blog.title, blog_path=blog.path)
		record.save()
		ActionRecordLog.objects.create(record=record)
		return record

	def abort(self, error):
		"""Close the record of the action due to an error having occurred.

		Arguments:
		error -- an ActionError instance

		"""

		# Record the reason for ending the record
		log = self.log
		log.error_message = str(error)
		log.base_error = error.error_info
		log.save()

		# Finalize the record
		self.ended = datetime.datetime.now()
		self.save()

	def finalize(self, blog):
		"""Finalize the record."""

		# Seal the record
		self.succeeded = True
		self.ended = datetime.datetime.now()
		self.save()

	@property
	def is_ended(self):
		"""True when the action has been ended, either from an error or success."""
		return self.ended is not None

	@property
	def is_failed(self):
		"""True when the action performed failed."""
		return self.is_ended and not self.succeeded

class ActionRecordLog(models.Model):
	"""A log of steps and actions that occurred during an action."""

	record        = models.OneToOneField(ActionRecord, verbose_name=_("action record"), related_name="log")
	error_message = models.TextField(null=True, blank=True, verbose_name=_("readable error message"))
	base_error    = models.TextField(null=True, blank=True, verbose_name=_("base exception message"))

	class Meta:

		app_label = "pressgang"
		verbose_name = _("action log")
		verbose_name_plural = _("action logs")

	def __unicode__(self):
		return _("log for %(record)s") % {'record': self.record}

	def start_action(self, step_name, message):
		"""Logs the start of an action that is part of a larger, multi-step action.

		Arguments:
		step_name -- the name of the step
		message -- the text of the message

		"""
		step = LogStep.objects.get_step(self, force_unicode(step_name))
		step.start_action(force_unicode(message))
		if settings.DEBUG:
			print _("Starting action: %(message)s") % {'message': message}

	def end_action(self, message):
		"""Logs the end of an action that is part of a larger, multi-step action.

		Arguments:
		message -- the text of the log message

		"""
		last_action = LogAction.objects.get_unclosed_action(self)
		if not last_action:
			raise PressGangError(_("You must call %(first)s after calling %(second)s") % {'first': 'start_action', 'second': 'end_action'})
		last_action.end(force_unicode(message))
		if settings.DEBUG:
			print _("Ending action: %(message)s") % {'message': message}
			print

	@property
	def ordered_steps(self):
		"""The steps in the log in numerical order."""
		return self.steps.order_by('order')

class LogStepManager(models.Manager):
	"""Custom manager for the LogStep model."""

	def get_step(self, log, name):
		"""Get or create the log step for the given record.

		Arguments:
		log -- an ActionRecordLog instance
		name -- the name of the step

		Returns: an instance of a LogStep model

		"""
		try:
			step = self.get(log=log, name=name)
		except LogStep.DoesNotExist:
			order = self.filter(log=log).count() + 1
			step = self.create(log=log, name=name, order=order)
		return step

class LogStep(models.Model):
	"""A step that is part of a larger action, such as an installation or upgrade."""

	objects = LogStepManager()

	log   = models.ForeignKey(ActionRecordLog, verbose_name=_("action log"), related_name="steps")
	name  = models.CharField(max_length=255, verbose_name=_("name"))
	order = models.PositiveSmallIntegerField(verbose_name=_("order"))

	class Meta:

		app_label = "pressgang"
		verbose_name = _("action log step")
		verbose_name_plural = _("action log steps")

	def __unicode__(self):
		return self.name

	def start_action(self, message):
		"""Log the start of an action.

		Arguments:
		message -- the text describing the start of the action

		Returns: a LogAction instance

		"""
		return LogAction.objects.create(log=self.log, step=self, start_message=message)

	@property
	def ordered_actions(self):
		"""All actions that are part of this step in their proper order."""
		return self.actions.order_by('order')

	@property
	def start_dt(self):
		"""The datetime at which the step was started."""
		try:
			return self.actions.order_by('started')[0].started
		except IndexError:
			return None

	@property
	def end_dt(self):
		"""The datetime at which the step was ended."""
		try:
			return self.actions.order_by('-started')[0].ended
		except IndexError:
			return None

	@property
	def is_complete(self):
		"""Whether or not the step is complete."""

		# If there is another step after this, or if this is the last step and
		# the record is marked as complete, consider this step complete
		complete = self.order < self.log.steps.order_by('-order')[0].order
		if not complete:
			complete = self.log.record.is_ended
		return complete

class LogActionManager(models.Manager):
	"""Custom manager for the LogAction model."""

	def get_unclosed_action(self, log):
		"""Get the unclosed action for the given log.

		Arguments:
		log -- an ActionRecordLog instance

		Returns: a LogAction instance with no end message or time or None

		"""
		try:
			return self.filter(log=log, ended__isnull=True)[0]
		except IndexError:
			return None

class LogAction(models.Model):
	"""An logged action that is part of an record."""

	objects = LogActionManager()

	log           = models.ForeignKey(ActionRecordLog, verbose_name=_("action log"))
	step          = models.ForeignKey(LogStep, verbose_name=_("step"), related_name="actions")
	start_message = models.TextField(verbose_name=_("start message"))
	started       = models.DateTimeField(auto_now_add=True, verbose_name=_("started"))
	end_message   = models.TextField(blank=True, null=True, verbose_name=_("end message"))
	ended         = models.DateTimeField(blank=True, null=True, verbose_name=_("completed"))
	order         = models.PositiveSmallIntegerField(verbose_name=_("order"))

	class Meta:

		app_label = "pressgang"
		verbose_name = _("action log action")
		verbose_name_plural = _("action log actions")

	def __unicode__(self):
		return self.start_message

	def save(self, *args, **kwargs):
		"""Keep track of the action's order."""

		# Update the action's order if we're inserting it
		if self.order is None:
			self.order = LogAction.objects.filter(step=self.step).count()

		super(LogAction, self).save(*args, **kwargs)

	def end(self, message):
		"""Logs the end of the action.

		Arguments:
		message -- the text of the ending message

		"""
		self.end_message = message
		self.ended = datetime.datetime.now()
		self.save()

	@property
	def is_complete(self):
		"""Whether or not the action has been completed."""
		return self.ended is not None
