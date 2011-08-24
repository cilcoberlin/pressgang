
import string

def safe_ascii():
	"""Provide a string of all safe ASCII characters.

	Returns: all ASCII characters except quotes and specials.

	"""
	allowed_chars = "".join([
			string.ascii_letters,
			string.digits,
			string.punctuation])
	forbidden_chars = ['"', "'", "\\", "/"]
	for forbidden_char in forbidden_chars:
		allowed_chars = allowed_chars.replace(forbidden_char, "")
	return allowed_chars

SAFE_ASCII = safe_ascii()

# A list of WordPress user roles, mapping a friendly name to the internal role ID
WP_ROLES = {
	'administrator': 'administrator',
	'author': 'author',
	'contributor': 'contributor',
	'editor': 'editor',
	'subscriber': 'subscriber'
}
