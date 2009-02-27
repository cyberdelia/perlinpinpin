#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import perlinpinpin
 
setup(name='perlinpinpin',
      version=perlinpinpin.__version__,
      py_modules = ['perlinpinpin'],
      license = 'MIT License',  
      author='Timothee Peignier',
      author_email='tim@tryphon.org',
      test_suite='tests'
)