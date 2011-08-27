
from pressgang.actions.install import InstallAction

class Install(InstallAction):
	"""Sample installer for a WordPress multisite installation."""

	display_name = "Multisite"
	wp_version = "3.1"
	multiple_blogs = True
	admin_email = "admin@example.com"

	class SiteOptions:

		first_post = "Welcome to your blog.  This is your first post."
		first_page = "Welcome to your first page."
		first_comment = "This is a default comment."
		first_comment_author = "A Commenter"

		new_user_account_email = """
Dear User,

An account has been created for you on the multisite blog called "SITE_NAME".

You can log in using the information below:

--------------------------------------------------------------------------------

Username: USERNAME
Password: PASSWORD
Login Link: LOGINLINK

--------------------------------------------------------------------------------

		"""

		new_blog_email = """
Dear User,

A blog has been created for you on the multisite blog called "SITE_NAME".

You can log in using the information below:

--------------------------------------------------------------------------------

Username: USERNAME
Password: PASSWORD
Login Link: BLOG_URLwp-login.php

--------------------------------------------------------------------------------

		"""

		send_admin_registration_notifications = False

		allowed_email_domains = [
			"example.com"
		]

		per_blog_upload_space_mbs = 100000
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

		available_themes = [
			"sample-theme"
		]

		allow_plugins_admin_menu = True

	class AllBlogOptions:

		akismet_key = "abcd1234"

		remove_default_page = True
		remove_default_comment = True

		plugins = [
			"sample-plugin.php"
		]

		description = "A sample multisite blog"

		enable_gravatars = True
		enable_threaded_comments = True

		timezone = "America/New_York"

	class ChildBlogOptions:

		sidebar_widgets = [
			"meta-2",
			"search-2"
		]

		theme = "sample-theme"

	class RootBlogOptions:

		theme = "sample-theme"

		sidebar_widgets = [
			"meta-2"
		]
