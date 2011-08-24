
from django.utils.translation import ugettext_lazy as _

from pressgang.actions.install.steps import InstallationStep
from pressgang.actions.install.exceptions import InstallationError
from pressgang.actions.options.exceptions import OptionsError
from pressgang.utils.apache import reload_apache

class Step(InstallationStep):

	name = _("WordPress customization")

	def execute(self, blog, installer):
		"""Brings the blog to a state where it can be visited."""

		# Attempt to apply the sitewide options if the blog is WPMU / multisite
		if blog.version.is_multi:
			self.start(_("Applying sitewide customizations."))
			try:
				installer.options.site.apply(blog)
			except OptionsError, e:
				raise InstallationError(_("The custom sitewide options could not be applied."), e)
			self.complete(_("Sitewide customizations applied."))

		# Create additional admin users if needed
		if installer.admins:
			for admin_email in installer.admins:
				self.start(_("Adding administrator %(email)s.") % {'email': admin_email})
				blog.add_admin(installer.provide_username(admin_email), admin_email)
				self.complete(_("Administrator added."))

		# Create non-admin users if requested, either adding a user to the root
		# blog or creating a blog for the user, depending on the type of blog
		if installer.users:
			is_multi = blog.version.is_multi
			for user_email in installer.users:
				self.start(_("Adding user %(email)s.") % {'email': user_email})
				if is_multi:
					blog.create_blog_for_user(
						installer.provide_username(user_email),
						user_email,
						installer.provide_user_blog_slug(user_email),
						installer.provide_child_blog_title(user_email))
				else:
					blog.add_user(installer.provide_username(user_email), user_email)
				self.complete(_("User added."))

		# Apply individual blog options
		if blog.version.is_multi:
			self.start(_("Applying all-blog customizations."))
			try:
				installer.options.all_blogs.apply(blog)
			except OptionsError, e:
				raise InstallationError(_("Sitewide blog customizations could not be applied."), e)
			self.complete(_("All-blog customizations applied."))
			self.start(_("Applying root-blog customizations."))
			try:
				installer.options.root_blog.apply(blog)
			except OptionsError, e:
				raise InstallationError(_("Root blog customizations could not be applied."), e)
			self.complete(_("Root-blog customizations applied."))
			self.start(_("Applying child-blog customizations."))
			try:
				installer.options.child_blogs.apply(blog)
			except OptionsError, e:
				raise InstallationError(_("Child-blog customizations could not be applied."), e)
			self.complete(_("Child-blog customizations applied."))
		else:
			self.complete(_("Applying blog customizations."))
			try:
				installer.options.blog.apply(blog)
			except OptionsError, e:
				raise InstallationError(_("Blog customizations could not be applied."), e)
			self.complete(_("Blog customizations applied."))

		# Restart Apache in the end to ensure a clean install
		self.start(_("Reloading Apache."))
		reload_apache()
		self.complete(_("Apache successfully reloaded."))
