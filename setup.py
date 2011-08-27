
from setuptools import setup, find_packages

setup(
	name='pressgang',
	version=__import__('pressgang').__version__,
	description='A WordPress installation manager.',
	author='Justin Locsei',
	author_email='justin.locsei@oberlin.edu',
	url='https://github.com/cilcoberlin/pressgang',
	download_url='https://github.com/cilcoberlin/pressgang/zipball/master',
	packages=find_packages(),
	package_data={'': ["*.*"]},
	include_package_data=True,
	zip_safe=False,
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Framework :: Django'
	]
)
