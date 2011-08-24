
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

register = template.Library()

def create_permission_filter(name, perm):
	"""Creates a filter to check if a user can perform a given task.

	The resulting filter will return True if the user has the given permission,
	and it can only be applied to an authenticated user instance.  If it is
	called on a non-User, a TemplateSyntaxError will be raised.

	Arguments:
	name -- the name under which to register the filter
	perm -- the name of a permission

	"""
	def permission_check(user):
		if user is None:
			return False
		if not isinstance(user, User):
			raise template.TemplateSyntaxError(_("%(filter)s may only be called on a User instance.") % {'filter': name})
		return user.has_perm(perm)
	register.filter(name, permission_check)

# Create filters to handle user permission checks
create_permission_filter('can_install_blogs', 'pressgang.can_install_blogs')
create_permission_filter('can_manage_blogs', 'pressgang.can_manage_blogs')
create_permission_filter('can_view_blogs', 'pressgang.can_view_blogs')

@register.simple_tag
def get_logout_url():
	"""Return the logout URL as set by the user."""
	return settings.LOGOUT_URL
