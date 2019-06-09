#!/usr/bin/env python

from setuptools import setup, find_packages

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(name='packagemanagerextension',
      version=version,
      description='Package Manager for Jupyter Notebook',
      author='Akash Ravi',
      author_email='akashkravi@gmail.com',
      url='https://github.com/techtocore/Jupyter-Package-manager',
      include_package_data=True,
      packages=find_packages(),
      zip_safe=False,
      )
