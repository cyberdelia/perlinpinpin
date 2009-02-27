#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import perlinpinpin
 
setup(name='perlinpinpin',
      version=perlinpinpin.__version__,
      description='Convert french fuzzy date to a python datetime object.',
      long_description="Convert from french fuzzy dates like 'hier', 'il y a 1 semaine et 1 jour', 'mardi prochain', '4 Janvier', etc., to a datetime object.",
      py_modules = ['perlinpinpin'],
      license = 'MIT License',
      keywords = "convert fuzzy date datetime time french",
      classifiers = [ "Development Status :: 4 - Beta",
                      "License :: OSI Approved :: MIT License",
                      "Operating System :: OS Independent",
                      "Programming Language :: Python",
                      "Topic :: Software Development :: Libraries :: Python Modules" ],
      author='Timothee Peignier',
      author_email='tim@tryphon.org',
      test_suite='tests'
)