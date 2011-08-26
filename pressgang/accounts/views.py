
from pressgang.utils.pages import Page

def access_denied(request):
	"""Shown to alert a user that access was denied to a particular page."""
	page = Page(request)
	return page.render('pressgang/accounts/denied.html')
