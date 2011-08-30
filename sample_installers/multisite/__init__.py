
from pressgang.actions.install import InstallAction

import datetime
import os

class Install(InstallAction):
	"""Sample installer for a WordPress multisite installation."""

	display_name = "Multisite"
	wp_version = "3.1"
	multiple_blogs = True
	admin_email = "admin@example.com"

	def provide_blog_dir(self):
		"""Place all blogs in a date-based multisite directory."""
		now = datetime.datetime.now()
		parts = ['multisite', now.year, now.month, now.day]
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

	def provide_child_blog_title(self, email):
		"""Make a title for a user's child blog influenced by their email."""
		return "%s's blog" % email.split("@")[0]

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
