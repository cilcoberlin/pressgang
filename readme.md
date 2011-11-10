PressGang WordPress Manager
===========================

PressGang is a Django application that makes it easier to manage multiple
WordPress installations on a single server.  It allows you to install blogs,
lock them down, manage users and perform easy rollbacks to previous versions.

PressGang can install any blogs using WordPress 3.0 or greater, and can still
perform some basic management tasks on older blogs.  **For the moment, it is only
capable of dealing with blogs installed in subdirectories, and does not support
subdomain installations.**

Installation
------------

**Installation**

    git clone git://github.com/cilcoberlin/pressgang.git
    python pressgang/setup.py install
    rm -R pressgang

**File Structure**

1. Create a new Django project.
2. Create a directory that is writable by your app to contain blog versions.
3. Create a directory that is writable by your app to contain per-blog Apache configuration files.
4. Copy the contents of the `media/` directory to your site's `media/` directory.

**Apache**

Somewhere in your Apache configuration file, add the following line, replacing
`CONFIG_DIR` with the full path to the directory created in step 2 of the
previous section:

    Include CONFIG_DIR/*.conf

Configuration
-------------

**Settings**

1. Add 'pressgang' to the `INSTALLED_APPS` list in your project's `settings.py` file.
2. Include 'pressgang.urls' in your project's URL configuration.
3. Provide values for the settings below.

`PRESSGANG_APACHE_CONFIGS_DIR`
A string of the absolute path to the directory that you created to hold per-blog Apache configuration files.

`PRESSGANG_APACHE_DOCUMENT_ROOT`
A string that should match the value of Apache's DocumentRoot.

`PRESSGANG_BACKUPS_DIR`
A string of the absolute path to the directory that you created to hold the blog backup files.

`PRESSGANG_DB_ADMIN_PASSWORD`
A string of the password for the admin use for your MySQL installation.

`PRESSGANG_DB_ADMIN_USER`
A string of the username of the admin user for your MySQL installation.

`PRESSGANG_INSTALLERS`
An optional list containing strings of the full paths to any custom installer
packages that you have created.  Each item in the list must be on your Python path.

`PRESSGANG_MYSQL_PATH`
The full path to your mysql executable.

`PRESSGANG_MYSQLDUMP_PATH`
The full path to your mysqldump executable.

`PRESSGANG_SERVER_BASE`
A string of the network location (i.e., 'subdomain.server.tld') of the server hosting your blogs.

**Standalone Settings***

If PressGang is the only application that you are running, you can use the following
values for your `settings.py` variables, replacing **PRESSGANG** with the optional
URL prefix of your PressGang site, if it is not running in the root of your site.

    LOGIN_URL  = 'PRESSGANG/accounts/login'
    LOGOUT_URL = 'PRESSGANG/accounts/logout'

To have PressGang handle any 404 or 500 errors, you can set the following values
in your main URL configuration.

    handler404 = 'pressgang.core.views.handle_404'
    handler500 = 'pressgang.core.views.handle_500'

**Permissions**

Any user that you add to your site must have certain permissions added to their
accounts through your project's admin site to be able to use PressGang.  The
possible permissions, given as how they show up in the list of permissions
available to users and groups, are:

`pressgang | blog | can install blogs`
Allows the user to install blogs

`pressgang | blog | can manage blogs`
Allows the user to make changes to the blogs.

`pressgang | blog | can view blogs`
Allows the user to view a list of all installed blogs.

Generally, a user will have all of the above permissions, but it is possible to
restrict the permissions if desired.

Custom Blog Installations
-------------------------

PressGang provides a flexible API that allows you to provide custom templates
for customizing the installation or upgrading of blogs.  These templates take
the form of standard Python packages and a few optional folders following a simple
file structure that PressGang uses to generate configuration rules for a blog.

To create a new template, make a Python package that appears somewhere in your
project's `PYTHONPATH`, making it available for import.  In the package's
`__init__.py` module, create a new class called `Install` that is descended from
`pressgang.actions.install.InstallAction`.  This class is the template for the
blog configuration.  It accepts a wide range of attributes and methods, and the
possible values and methods for the class can be figured out by consulting the
source code for `pressgang.actions.install.InstallAction` and the sample installers
available in the `sample_installers` package.

In addition to the above attributes and methods, the `Install` class can also
take options classes in the same manner that a Django model receives `Meta` options.
For examples of how to use and set these options, consult the values of the
`SiteOptions`, `AllBlogOptions`, `ChildBlogOptions`, `RootBlogOptions` and `BlogOptions`
classes used by the sample installers defined in the `sample_installers` package.

Once you have created a template in Python, you can provide additional PHP files
that should be copied to the blog via the `mu-plugins/`, `plugins/` and `themes/`
directories that can exist in your template's package.  The contents of each
directory get copied to the `wp-content/mu-plugins/` directory of the blog.

With your installer created, you now need to tell PressGang that it exists.  To
do so, simply add the import path to your package to the `PRESSGANG_INSTALLERS`
list in your project's `settings.py` file.  It will now appear in the list of
available installation template when you are using PressGang.
