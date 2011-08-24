
import re
import urlparse

def url_join(*parts):
	"""Join the URL components passed.

	Arguments:
	parts -- a list of URL components

	Returns: a joined URL, which will always end with a '/' if it's a non-file URL

	"""
	url_parts = list(urlparse.urlparse("/".join(parts)))
	url_parts[2] = re.sub(r'\/{2,}', '/', url_parts[2])
	url = urlparse.urlunparse(url_parts)
	if not re.search(r'\.[a-zA-Z0-9]$', url) and not url.endswith('/'):
		url = "%s/" % url
	return url
