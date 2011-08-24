
from django.template.loader import render_to_string
from django.utils.importlib import import_module

from pressgang.actions.options import Option, Options
from pressgang.utils.registry import create_registry

import os

BlogOptionRegistry = create_registry('id')

class BlogOption(Option):
	"""Base class for a single blog option."""

	__metaclass__ = BlogOptionRegistry

	# The path to the blog-options template directory
	_BLOG_OPTIONS_TEMPLATE_DIR = "pressgang/options/blog"

	# The name of the template file used to render the plugin, relative to the
	# root blog-options template directory
	template = None

	def generate_code(self, blog, value):
		"""Add code for a plugin to apply the WordPress option.

		Arguments:
		blog -- an instance of a Blog object
		value -- the value of the option as a Python data type

		Returns: PHP code to apply the option

		"""

		# Since blog options vary more widely than site options, search for a
		# specific template for the option.  If none is found, use the default
		# blog-option template.
		template = 'pressgang/options/blog_option.php'
		if self.template:
			template = os.path.join(self._BLOG_OPTIONS_TEMPLATE_DIR, self.template)
		return render_to_string(template, {
			'blog':  blog,
			'name':  self.name,
			'option': self.id,
			'value': self.provide_wp_value(value) or value
		})

class BlogOptions(Options):
	"""Options for the blog."""

	# Whether the options apply to the root blog
	for_root = True

	# Whether the options apply to non-root blogs
	for_non_root = False

	def get_option_obj(self, option):

		# Import the module containing the options, so that the registry is
		# able to add each option to its list
		import_module('pressgang.actions.options.blog.options')

		# Attempt to get the blog option
		try:
			return BlogOption.get_registry_item(option)
		except ValueError:
			return None

	def render_plugin_code(self, blog, code):
		return render_to_string('pressgang/options/blog_options.php', {
			'blog':         blog,
			'code':         code,
			'for_root':     self.for_root,
			'for_non_root': self.for_non_root,
			'options':      self.__class__.__name__.lower()
		})

class RootBlogOptions(BlogOptions):
	"""Options for the root blog."""

	for_root = True
	for_non_root = False

class AllBlogOptions(BlogOptions):
	"""Options for all blogs on the site."""

	for_root = True
	for_non_root = True

class ChildBlogOptions(BlogOptions):
	"""Options for all blogs except the root one."""

	for_root = False
	for_non_root = True
