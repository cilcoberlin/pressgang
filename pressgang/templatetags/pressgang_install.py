
from django import template
from django.contrib.auth.models import User

from pressgang.utils.constants import SAFE_ASCII

register = template.Library()

# The length of a WordPress key as it appears in the wp-config file
_WP_KEY_LENGTH = 64

@register.simple_tag
def generate_key():
	"""Generate a complex value to be used as a key or salt by WordPress."""
	return User.objects.make_random_password(_WP_KEY_LENGTH, SAFE_ASCII)
