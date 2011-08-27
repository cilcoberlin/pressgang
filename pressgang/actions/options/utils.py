
from pressgang.actions.options.blog import BlogOptions, AllBlogOptions

def sitewide_activate_plugin(plugin, blog):
	"""Activates a per-blog plugin on every blog on the given blog's network.

	If the plugin cannot be activated, a PressGangError is raised.

	Arguments:
	plugin -- the path to the plugin, relative to the blog's plugins directory
	blog -- a Blog instance

	"""
	Options = BlogOptions if blog.version.is_multi else AllBlogOptions
	options = Options({'plugins': [plugin]})
	options.apply(blog)
