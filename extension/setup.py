#!/usr/bin/env python

from setuptools import setup, find_packages

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(name='packagemanagerextension',
      version=version,
      description='Jupyter notebook extension to manage packages in SWAN projects',
      author='Akash Ravi',
      author_email='akashkravi@gmail.com',
      url='https://github.com/techtocore/Jupyter-Package-Manager',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'conda >= 4.5',
          'notebook >=4.3.1',
          'packaging',
          'pyyaml'
      ],
      )
