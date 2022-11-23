from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in jmi/__init__.py
from jmi import __version__ as version

setup(
	name="jmi",
	version=version,
	description="Custom App for JMI",
	author="TEAMPRO",
	author_email="hr@groupteampro.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
