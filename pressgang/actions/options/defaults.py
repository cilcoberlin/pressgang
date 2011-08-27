
class SiteOptions:
	"""Options for the site.

	These settings are only applied to a WPMU or multisite blog.
	"""

	# Allow the plugins menu to be available to non-root blogs
	# ----
	# Example: allow_plugins_admin_menu = True
	allow_plugins_admin_menu = None

	# A list of email domains that can be used to register a new blog
	# ----
	# Example: allowed_email_domains = ["example.com", "example.com"]
	allowed_email_domains = None

	# A list of allowed file extensions as strings without a dot for uploading
	# ----
	# Example: allowed_upload_file_types = ["xls", "doc"]
	allowed_upload_file_types = None

	# Themes available to blogs, given as the name of the theme folder
	# ----
	# Example: available_themes = ["twentyten", "kubrick"]
	available_themes = None

	# A list of email domains that cannot be used to register a blog
	# ----
	# Example: banned_email_domains = ["banned.com", "banned2.com"]
	banned_email_domains = None

	# A list of usernames that a user cannot register with
	# ----
	# Example: banned_usernames = ["banned", "forbidden"]
	banned_usernames = [
		"www",
		"web",
		"root",
		"admin",
		"main",
		"invite",
		"administrator",
		"files",
		"blog"
	]

	# The text of the default first comment on a newly created blog
	# ----
	# Example: first_comment = "This is your first comment"
	first_comment = None

	# The name of the author of the default comment
	# ----
	# Example: first_comment_author = "Default comment author"
	first_comment_author = None

	# The URL of the first comment author
	# ----
	# Example: first_comment_url = "http://www.test.com"
	first_comment_url = None

	# The text of the default first page created for the blog
	# ----
	# Example: first_page = "This is your first page"
	first_page = None

	# The text of the default post on a newly created blog
	# ----
	# Example: first_post = "This is your first post"
	first_post = None

	# The maximum allowed size of an upload file, as an int in kilobytes
	# ----
	# Example: max_file_upload_size_kbs = 10000
	max_file_upload_size_kbs = None

	# The available media-upload buttons
	# ----
	# Example: media_upload_buttons = ["image", "video", "audio"]
	media_upload_buttons = None

	# The text of the email sent to a user when a blog is created for them
	# ----
	# Example: new_blog_email = "You have a new blog"
	new_blog_email = None

	# The text of the email sent to a user when their account is created
	# ----
	# Example: new_user_account_email = "You have a new user account"
	new_user_account_email = None

	# The upload space allowed for each blog, as an int in megabytes
	# ----
	# Example: per_blog_upload_space_mbs = 100
	per_blog_upload_space_mbs = None

	# A boolean of whether or not the admin should receive email notifications
	# ----
	# Example: send_admin_registration_notifications = True
	send_admin_registration_notifications = None

class BlogOptions:
	"""Options for the blog.

	If use_multiple_blogs is false, these options are applied to the single
	WordPress blog hosted by this installation.  If use_multiple_blogs is true,
	and any of the multiple-blog-specific options keys are not used, these values
	will be used to customize every blog on the site.
	"""

	# The value of an Akismet API key
	# ----
	# Example: akismet_key = "abcd12345"
	akismet_key = None

	# The title of the default page
	# ----
	# Example: default_page_title = "My default page"
	default_page_title = None

	# The description of the blog
	# ----
	# Example: description = "Blog description"
	description = None

	# Whether or not to enable gravatars
	# ----
	# Example: enable_gravatars = True
	enable_gravatars = None

	# Whether or not to enable threaded comments
	# ----
	# Example: enable_threaded_comments = True
	enable_threaded_comments = None

	# Whether or not the blog is visible to search engines
	# ----
	# Example: is_public = True
	is_public = None

	# A list of plugins to enable, given as the path to the plugin's .php file
	# relative to the wp-content/plugins directory
	# ----
	# Example: plugins = ["akismet/akismet.php", "folder/plugin.php"]
	plugins = None

	# Whether or not to remove the default first comment
	# ----
	# Example: remove_default_comment = True
	remove_default_comment = None

	# Whether or not to remove the default page
	# ----
	# Example: remove_default_page = True
	remove_default_page = None

	# Whether or not to remove the default first post
	# ----
	# Example: remove_default_post = True
	remove_default_post = None

	# A list of sidebar widgets to use, given as the widget ID
	# ----
	# These widgets are applied to the first sidebar declared in the theme, or
	# are simply ignored if the theme provides no sidebars
	# ----
	# Example: sidebar_widgets = ["meta-2", "search-2", "widget_id"]
	sidebar_widgets = None

	# The activated theme, identified by theme folder name
	# ----
	# Example: theme = "twentyten"
	theme = None

	# The timezone string to use for the blog
	# ----
	# Example: timezone = "America/New_York"
	timezone = None

class RootBlogOptions(BlogOptions):
	"""Options for the root blog.

	These settings are only used if `multiple_blogs` is True.
	"""
	pass

class AllBlogOptions(BlogOptions):
	"""Options for all blogs on the site.

	These settings are only used if `multiple_blogs` is True.
	"""
	pass

class ChildBlogOptions(BlogOptions):
	"""Options for all blogs except the root one.

	These settings are only used if `multiple_blogs` is True.
	"""
	pass
