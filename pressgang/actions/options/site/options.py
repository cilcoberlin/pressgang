
from django.utils.translation import ugettext_lazy as _

import pressgang.actions.options.defaults as default_options
from pressgang.actions.options.site import SiteOption

class FirstPost(SiteOption):
	"""The content of the default first post left on a newly created blog."""

	id = "first_post"
	name = _("default post text")
	wp_id = "first_post"

class FirstPage(SiteOption):
	"""The content of the default first page on a newly created blog ."""

	id = "first_page"
	name = _("default page text")
	wp_id = "first_page"

class FirstComment(SiteOption):
	"""The content of the default comment on a newly created blog ."""

	id = "first_comment"
	name = _("default comment text")
	wp_id = "first_comment"

class FirstCommentAuthor(SiteOption):
	"""The name of the author of the default comment on a newly created blog ."""

	id = "first_comment_author"
	name = _("default comment author name")
	wp_id = "first_comment_author"

class FirstCommentURL(SiteOption):
	"""The URL of the author of the default comment on a newly created blog ."""

	id = "first_comment_url"
	name = _("default comment author URL")
	wp_id = "first_comment_url"

class SendAdminNotifications(SiteOption):
	"""Whether or not to send notifications to the administrator."""

	id = "send_admin_registration_notifications"
	name = _("send email notifications to admin")
	wp_id = "registrationnotification"

	def provide_wp_value(self, value):
		"""Convert True to 'yes' and False to 'no'."""
		if value:
			return 'yes'
		else:
			return 'no'

class NewUserEmail(SiteOption):
	"""The text of the email sent to a newly created user."""

	id = "new_user_account_email"
	name = _("email to send to a new user")
	wp_id = "welcome_user_email"

class AllowedEmailDomains(SiteOption):
	"""Email domains allowed for users."""

	id = "allowed_email_domains"
	name = _("valid email domains for new users")
	wp_id = "limited_email_domains"

class BannedEmailDomains(SiteOption):
	"""Email domains that are not allowed for users."""

	id = "banned_email_domains"
	name = _("invalid email domains for new users")
	wp_id = "banned_email_domains"

class BannedUsernames(SiteOption):
	"""Usernames that are not available to a user."""

	id = "banned_usernames"
	name = _("banned usernames")
	wp_id = "illegal_names"

	def provide_wp_value(self, value):
		"""Combine the user-provided value with the default."""
		value.extend(default_options.SiteOptions.banned_usernames)
		return list(set(value))

class PerBlogUploadSpace(SiteOption):
	"""The amount of upload space available for each blog."""

	id = "per_blog_upload_space_mbs"
	name = _("per-blog upload space, in megabytes")
	wp_id = "blog_upload_space"

class MaxFileUploadSize(SiteOption):
	"""The maximum size of an uploaded file."""

	id = "max_file_upload_size_kbs"
	name = _("the maximum size of an uploaded file")
	wp_id = "fileupload_maxk"

class AllowedUploadFileTypes(SiteOption):
	"""File types that can be uploaded."""

	id = "allowed_upload_file_types"
	name = _("allowed file-upload types")
	wp_id = "upload_filetypes"

	def provide_wp_value(self, value):
		"""Make the list a space-separated string."""
		return " ".join(value)

class MediaUploadButtons(SiteOption):
	"""The media-upload buttons available."""

	id = "media_upload_buttons"
	name = _("available media-upload buttons")
	wp_id = "mu_media_buttons"

	def provide_wp_value(self, buttons):
		"""Provide the list as dict keyed by button with true string values."""
		return dict(zip(buttons, ["1"] * len(buttons)))

class NewBlogEmail(SiteOption):
	"""The text of the email sent to a user with a newly created blog."""

	id = "new_blog_email"
	name = _("the email sent to a user with a new blog")
	wp_id = "welcome_email"

class AvailableThemes(SiteOption):
	"""The themes that a user can select as their blog theme."""

	id = "available_themes"
	name = _("available themes")
	wp_id = "allowedthemes"

	def provide_wp_value(self, themes):
		"""Provide the list as dict keyed by theme with True values."""
		return dict(zip(themes, [True] * len(themes)))

class AllowPluginsAdminMenu(SiteOption):
	"""Whether or not the plugins menu is available on the admin side."""

	id = "allow_plugins_admin_menu"
	name = _("allow plugins admin menu")
	wp_id = "menu_items"

	def provide_wp_value(self, value):
		"""Enable the plugins menu by making it the only admin menu."""
		if value:
			return {'plugins': "1"}
		else:
			return []
