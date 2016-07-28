#!/usr/bin/env python
"""msg package installer.

"""

import sys
from setuptools import setup
from distutils.version import StrictVersion

from pip.req import parse_requirements

from msg import __version__


# Here I am lazy; I really didn't want to maintain the depends
# in both requirements files AND in this setup, thus we are
# going to read them all into a list.
#
# CREDIT: http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool
#
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements/develop.txt', session=False)
# reqs is a list of requiremens
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='msg',
      packages=['msg'],
      version=__version__,
      description='msg server backend',
      setup_requires=['setuptools-markdown'],
      long_description_markdown_filename='README.md',
      author='Lily Seabreeze',
      author_email='lillian.gardenia.seabreeze@gmail.com',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                  ],
    )

