
def create_registry(attr_name):
	"""Create a new registry type that tracks objects by the given attribute name.

	Arguments:
	attr_name -- the string name of the attribute by which to key the registry

	"""

	class Registry(type):
		"""An abstract registry for objects keyed by an attribute value."""

		_registered = {}

		def __init__(self, name, bases, attrs):
			"""Update our object registry, keyed by an attribute value."""

			super(Registry, self).__init__(name, bases, attrs)

			# Don't track the original class that declared the registry
			if getattr(bases[0], '__metaclass__', None) != Registry:
				return

			if not attrs.get(attr_name, None):
				raise TypeError("You must define a '%(attr)s' for the %(class)s class" % {'attr': attr_name, 'class': name})
			attr_val = attrs[attr_name]
			if attr_val in self._registered:
				raise TypeError("You cannot have more than one %(class) class with a '%(attr)s' of '%(val)s'" % {'class': name, 'attr': attr_name, 'val': attr_val})

			self._registered[attr_val] = self

		@classmethod
		def get_registry_item(self, attr_val):
			"""Return the class registered under the given attribute name.

			If the class instance cannot be found, a ValueError is raised.
			"""
			try:
				return self._registered[attr_val]
			except KeyError:
				raise ValueError("No class instance could be found for '%(attr)s'" % {'attr': attr_val})

	return Registry
