
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from pressgang.core.exceptions import PressGangConfigurationError
from pressgang.actions.options.exceptions import OptionsError

import inspect
import os

class ActionWithOptions(type):
	"""The metaclass for an action that defines WordPress options."""

	# A mapping of class names to keys in the `options` dict, with the key being
	# the name of the setting as it will appear on an action, and the value a
	# tuple containing the value of the options package in which the actual
	# Options-descended class is defined and the dictionary key on the action's
	# `options` member through which the settings can be accessed
	_OPTION_KEYS = {
		'SiteOptions':      ('site', 'site'),
		'BlogOptions':      ('blog', 'blog'),
		'RootBlogOptions':  ('blog', 'root_blog'),
		'AllBlogOptions':   ('blog', 'all_blogs'),
		'ChildBlogOptions': ('blog', 'child_blogs')
	}

	def __new__(cls, name, bases, attrs):
		"""Provide the class with settings."""

		# Combine our options and provide them to the class
		if 'options' in attrs:
			raise PressGangConfigurationError(_("The action %(action)s cannot have a class member named %(name)s.  Please use a different name.") % {'action': name, 'name': 'options'})
		attrs['options'] = cls.merge_options(attrs)

		return super(ActionWithOptions, cls).__new__(cls, name, bases, attrs)

	@classmethod
	def merge_options(cls, attrs):
		"""Combine the default and user options for an action.

		The options will be returned as an object with members for each option type,
		whose value will be an Options instance.  The possible members are:

		    site 	    - site options
		    blog        - blog options
		    root_blog   - root blog options
		    all_blogs   - options applied to all blogs
		    child_blogs - options applied to all non-root blogs

		Returns: a class defining options

		"""

		import pressgang.actions.options.defaults as default_options
		import pressgang.actions.options.blog as blog_options
		import pressgang.actions.options.site as site_options

		# Create option instances for each option by combining the default options
		# with any options specified on the current action class
		all_options = {}
		for class_option, option_info in cls._OPTION_KEYS.iteritems():
			option_args = {}

			# Build the options dict to pass when creating an options instance
			# built from the members of the default options class and the user-
			# specified options of the current action
			user_options = attrs.get(class_option, None)
			options = getattr(default_options, class_option)
			for member in inspect.getmembers(options):
				if not member[0].startswith('__'):
					option_args[member[0]] = getattr(user_options, member[0], member[1])

			# Create an options instance whose type matches the current option
			options_package = blog_options if option_info[0] == 'blog' else site_options
			OptionsClass = getattr(options_package, class_option)
			all_options[option_info[1]] = OptionsClass(option_args)

		# Provide the options as an object
		class OptionsObject:
			pass
		for option_name, options in all_options.iteritems():
			setattr(OptionsObject, option_name, options)
		return OptionsObject

class Options(object):
	"""Base class for any options."""

	# The plugin file name used to apply the options
	_PLUGIN_FILE = "pressgang.php"

	def __init__(self, options):
		"""Creates a new options instance.

		Argumnents:
		options -- a dict of option names and values

		"""
		self._options = self._normalize_options(options)

	def _normalize_options(self, options):
		"""Normalizes a dict of option key / value pairs.

		Normalization in this case consists largely of stripping initial and
		terminal whitespace from strings.

		Returns: a dict of normalized options

		"""
		for name, value in options.iteritems():
			try:
				options[name] = value.strip()
			except AttributeError:
				pass
		return options

	def update_option(self, id, value):
		"""Updates the value of an option.

		Since all options are populated with all possible keys, if the given
		id is not found in those options, an OptionsError is raised.

		Arguments:
		id -- the ID of an option
		value -- the value of the option

		"""
		if id not in self._options:
			raise OptionsError(_("%(id)s is not a valid %(type)s option ID") % {'id': id, 'type': self.__class__.__name__})
		self._options[id] = value

	def apply(self, blog, force=False):
		"""Applies the options to a blog.

		The `force` kwarg is important, as it overrides some of the safety checks
		that PressGang performs before applying options.  By default, if a blog
		is unmanaged, or if a blog or site has already had options applied to
		it, no further customization is done.  Passing a value of True for `force`,
		however, bypasses these checks and forces the options to be applied.

		Arguments:
		blog -- an instance of a Blog object

		Keyword Arguments:
		force -- a boolean of whether or not to force application of options

		"""

		# If the blog is not managed, don't bother applying options, as the
		# potential for destruction is simply too great
		if not force and not blog.is_managed:
			return

		# Build a list of all generated code to set each option
		code = []
		for name, value in self._options.iteritems():
			if value is not None:
				Option = self.get_option_obj(name)
				if Option:
					option = Option()
					code.append(option.generate_code(blog, value))

		# Apply the options, if there are any to apply
		if code:
			blog.apply_changes(self.render_plugin_code(blog, "\n".join(code), force))

	def render_plugin_code(self, blog, code):
		"""Render the PHP code used for the plugin.

		Note that the value of `code` will not be wrapped in <php> tags, so the
		minimum that this function must do when defined by a child Option is
		to wrap the code in <php> tags.

		Arguments:
		blog -- an instance of a Blog object
		code -- the PHP code fragment to set the options

		Returns: fully parsable PHP code to apply the options

		"""
		raise NotImplementedError

	def get_option_obj(self, option):
		"""Gets an Option object that defines how to apply the given option name.

		Arguments:
		option -- the name of an option defined in an actions options

		Returns: an instance of an option-descended object or None

		"""
		raise NotImplementedError

class Option(object):
	"""Base class for a single configurable option.

	Any options descended from this must define a few members.  First, they must
	provide an `id` and a `name`, being the option's internal identifier and
	its display name, respectively.  Lastly, they must define an `apply` method
	that
	"""

	# The name of the option when specified in an action's options
	id = None

	# The display name of the option
	name = None

	def generate_code(self, blog, value):
		"""Generate PHP code to apply the option in WordPress.

		This must be defined by each option, and will generally be the only
		method that they override.

		Arguments:
		blog -- an instance of a Blog object
		value -- the value of the option

		Returns: a string containing PHP code to apply the option

		"""
		raise NotImplementedError

	def provide_wp_value(self, value):
		"""Allows an option to provide a dynamic value for the option value.

		If an option overrides this function to return a value, that value will
		be given preference over the raw value.

		Arguments:
		blog -- an instance of a Blog object

		Returns: a transformed value for the option's value

		"""
		return None


