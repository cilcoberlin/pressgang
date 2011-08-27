
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.options.blog import BlogOption

class AkismetKey(BlogOption):
	"""The Akismet API key to use."""

	id = "akismet_key"
	name = _("akismet API key")
	template = "akismet_key.php"

class DefaultPageTitle(BlogOption):
	"""The title of the default page."""

	id = "default_page_title"
	name = _("default page title")
	template = "default_page_title.php"

class Description(BlogOption):
	"""The blog's description or byline."""

	id = "description"
	name = _("blog description")
	template = "description.php"

class EnableGravatars(BlogOption):
	"""Whether or not to enable gravatars."""

	id = "enable_gravatars"
	name = _("enable gravatars")
	template = "enable_gravatars.php"

class EnableThreadedComments(BlogOption):
	"""Whether or not to enable threaded comments."""

	id = "enable_threaded_comments"
	name = _("enable threaded comments")
	template = "enable_threaded_comments.php"

class IsPublic(BlogOption):
	"""Whether or not the blog is visible to search engines."""

	id = "is_public"
	name = _("blog is visible to search engines")
	template = "is_public.php"

	def provide_wp_value(self, value):
		"""Convert boolean values to integers."""
		return int(value)

class Plugins(BlogOption):
	"""Which plugins to activate."""

	id = "plugins"
	name = _("plugins to activate")
	template = "plugins.php"

class RemoveDefaultPage(BlogOption):
	"""Whether or not to remove the default page."""

	id = "remove_default_page"
	name = _("remove default page")
	template = "remove_default_page.php"

class RemoveDefaultComment(BlogOption):
	"""Whether or not to remove the default comment."""

	id = "remove_default_comment"
	name = _("remove default comment")
	template = "remove_default_comment.php"

class RemoveDefaultPost(BlogOption):
	"""Whether or not to remove the default post."""

	id = "remove_default_post"
	name = _("remove default post")
	template = "remove_default_post.php"

class SidebarWidgets(BlogOption):
	"""Which widgets to enable in the first available sidebar."""

	id = "sidebar_widgets"
	name = _("default sidebar widgets")
	template = "sidebar_widgets.php"

class Theme(BlogOption):
	"""The activated theme for the blog."""

	id = "theme"
	name = _("activated theme")
	template = "theme.php"

class Timezone(BlogOption):
	"""The time zone to use for the blog."""

	id = "timezone"
	name = _("time zone")
	template = "timezone.php"
