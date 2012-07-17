
from django.template.loader import render_to_string
from django.utils.importlib import import_module

from pressgang.actions.options import Option, Options
from pressgang.utils.registry import create_registry

SiteOptionRegistry = create_registry('id')

class SiteOption(Option):
	"""Base class for a single site option."""

	__metaclass__ = SiteOptionRegistry

	# The databse ID used by WordPress for the site option
	wp_id = None

	# A custom template to use to set the option, relative to the site-options
	# template directory
	template = None

	# Whether the option is only available on multisite installations
	multisite_only = False

	def generate_code(self, blog, value):
		"""Add code for a plugin to apply the WordPress option.

		Arguments:
		blog -- an instance of a Blog object
		value -- the value of the option as a Python data type

		"""

		# If the option is only available on multisite, provide no code
		if self.multisite_only and not blog.version.is_multi:
			return ""

		# Use a custom template if one was provided, or fall back to the default
		if self.template:
			template = 'pressgang/options/site/%s' % self.template
		else:
			template = 'pressgang/options/site_option.php'

		return render_to_string(template, {
			'option': self.provide_wp_id(blog) or self.wp_id,
			'name': self.name,
			'value': self.provide_wp_value(value) or value
		})

	def provide_wp_id(self, blog):
		"""Allows an option to provide a dynamic value for the WordPress database ID.

		If an option overrides this function to return a value, that value will
		be given preference over the value of the option's `wp_id`.

		Arguments:
		blog -- an instance of a Blog object

		Returns: a string of the database ID of the option

		"""
		return None

class SiteOptions(Options):
	"""Options for the site."""

	def get_option_obj(self, option):

		# Import the module containing the options, so that the registry is
		# able to add each option to its list
		import_module('pressgang.actions.options.site.options')

		# Attempt to return the requested option
		try:
			return SiteOption.get_registry_item(option)
		except ValueError:
			return None

	def render_plugin_code(self, blog, code, force):
		return render_to_string('pressgang/options/site_options.php', {
			'code': code,
			'force': force,
			'options': self.__class__.__name__.lower()
		})
