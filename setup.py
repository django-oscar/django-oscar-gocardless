#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-oscar-gocardless',
      version='0.1',
      url='https://github.com/tangentlabs/django-oscar-gocardless',
      author="David Winterbottom",
      author_email="david.winterbottom@tangentlabs.co.uk",
      description="GoCardLess payment module for django-oscar",
      long_description=open('README.rst').read(),
      keywords="Payment, GoCardLess",
      license='BSD',
      packages=find_packages(),
      install_requires=['gocardless']
      )
