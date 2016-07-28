#!/usr/bin/env python
"""msg package installer.

"""

import sys
from setuptools import setup


# demon magic to get version without activating
# imports
exec(open('msg/__init__.py').read())
setup(name='msg',
      packages=['msg'],
      version=__version__,
      description='msg server backend',
      setup_requires=['setuptools-markdown',],
      install_requires=['flask', 'flask_sqlalchemy',
                        'flask_sqlalchemy', 'flask_limiter', 'flask-restful',
                        'flask-httpauth', 'requests', 'flask_sse',
                        'gunicorn', 'jsonschema'],
      long_description_markdown_filename='README.md',
      author='Lily Seabreeze',
      author_email='lillian.gardenia.seabreeze@gmail.com',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                  ],
    )
