
from django.contrib.auth.models import User

class PressGangUser(User):
	"""Proxy user for a PressGang user."""

	class Meta:
		proxy = True

	def can_install_blogs(self):
		"""Return True if the user can install new blogs."""
		return self.has_perm('pressgang.can_install_blogs')

	def can_manage_blogs(self):
		"""Return True if the user can apply changes to blogs."""
		return self.has_perm('pressgang.can_manage_blogs')

	def can_view_blogs(self):
		"""Return True if the user can view a list of installed blogs."""
		return self.has_perm('pressgang.can_view_blogs')
