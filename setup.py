#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup, Command
from unittest import TextTestRunner, TestLoader

import perlinpinpin


class TestCommand(Command):
    description = "run unit tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run unit tests"""
        tests = TestLoader().loadTestsFromName('tests')
        t = TextTestRunner(verbosity=1)
        t.run(tests)


setup(name='perlinpinpin',
      version=perlinpinpin.__version__,
      description='Convert french fuzzy date to a python date object.',
      long_description="Convert from french fuzzy dates like 'hier', 'il y a 1 semaine et 1 jour', 'mardi prochain', '4 Janvier', etc., to a date object.",
      py_modules=['perlinpinpin'],
      license='BSD License',
      url='http://cyberdelia.github.com/perlinpinpin/',
      keywords="convert fuzzy date time french",
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules"],
      author='Timothee Peignier',
      author_email='tim@tryphon.org',
      cmdclass={'test': TestCommand}
)
