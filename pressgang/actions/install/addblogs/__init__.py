
from django.utils.translation import ugettext_lazy as _

from pressgang.actions import Action
from pressgang.actions.install.addblogs.models import BlogAdditionRecord

class AddBlogsAction(Action):
	"""An action for reverting a blog to a previous version snapshot."""

	display_name = _("child blog addition")

	Record = BlogAdditionRecord

	log_template = "pressgang/addblogs/record.html"
	execute_template = "pressgang/addblogs/addblogs.html"

	steps = [
		'pressgang.actions.install.addblogs.steps.addblogs',
	]

	def __init__(self, *args, **kwargs):
		"""Create a new blog addition action.

		Keyword Arguments:
		users -- a list of user emails
		blog_type -- an Installer instance

		"""
		self.users = kwargs.pop('users', [])
		self.blog_type = kwargs.pop('blog_type', None)
		self.new_blog_count = len(self.users)
		super(AddBlogsAction, self).__init__(*args, **kwargs)
