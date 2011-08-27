
from pressgang.actions.install import InstallAction

class Install(InstallAction):
	"""Sample installer for a standard WordPress installation."""

	display_name = "Single"
	wp_version = "3.1"
	admin_email = "admin@example.com"

	class SiteOptions:

		first_post = "Welcome to your blog.  This is your first post."
		first_page = "Welcome to your first page."
		first_comment = "This is a default comment."
		first_comment_author = "A Commenter"

		new_user_account_email = """
Dear User,

An account has been created for you on the blog called "SITE_NAME".

You can log in using the information below:

--------------------------------------------------------------------------------

Username: USERNAME
Password: PASSWORD
Login Link: LOGINLINK

--------------------------------------------------------------------------------

		"""

		send_admin_registration_notifications = False

		allowed_email_domains = [
			"example.com"
		]

		max_file_upload_size_kbs = 15000

		allowed_upload_file_types = [
			"jpg",
			"jpeg",
			"png",
			"gif",
			"mp3",
			"mov",
			"avi",
			"wmv",
			"pdf",
			"doc",
			"docx",
			"ppt",
			"pptx",
			"mp4",
			"m4a",
			"m4v",
			"rtf",
			"txt",
			"xls",
			"xlsx"
		]

		media_upload_buttons = [
			"image",
			"video",
			"audio"
		]

	class BlogOptions:

		akismet_key = "abcd1234"

		remove_default_page = True
		remove_default_comment = True

		plugins = [
			"sample-plugin.php"
		]

		description = "A sample blog"

		enable_gravatars = True
		enable_threaded_comments = True

		timezone = "America/New_York"

		sidebar_widgets = [
			"meta-2",
			"search-2"
		]

		theme = "sample-theme"
