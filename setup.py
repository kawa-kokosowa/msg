#!/usr/bin/env python
"""msgboard package installer.

"""

import sys
from setuptools import setup
from distutils.version import StrictVersion

from msgboard import __version__


setup(name='msgboard',
      packages=['msgboard'],
      version=__version__,
      description='msgboard server backend',
      setup_requires=['setuptools-markdown'],
      long_description_markdown_filename='README.md',
      author='Lillian Seabreeze',
      author_email='lillian.gardenia.seabreeze@gmail.com',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                  ],
    )

