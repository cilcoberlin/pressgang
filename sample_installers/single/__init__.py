
from pressgang.actions.install import InstallAction

import datetime
import os

class Install(InstallAction):
	"""Sample installer for a standard WordPress installation."""

	display_name = "Single"
	wp_version = "3.1"
	admin_email = "admin@example.com"

	def provide_blog_dir(self):
		"""Place all blogs in a date-based single-blog directory."""
		now = datetime.datetime.now()
		parts = ['single', now.year, now.month, now.day]
		return os.path.join(*[str(part) for part in parts])

	def provide_db_base_name(self):
		"""Use a database name influenced by the first initial of the blog's slug."""
		return self.slug[0]

	def provide_db_user_base_name(self):
		"""Have the database user's name influenced by the blog slug."""
		return "%s_admin" % self.slug

	def provide_wp_username(self, email):
		"""
		Give a user a WordPress username that attempts to create a user ID from
		the first initial of a user's first name and the first five letters of
		their last name, if their email address appears to be a first.last@example.com
		email address, or simply uses their whole non-domain email address.
		"""
		name = email.split("@")[0]
		name_parts = name.split(".")
		if len(name_parts) > 1:
			return "%s%s" % (name_parts[0][0], name_parts[-1][:5])
		else:
			return name

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
