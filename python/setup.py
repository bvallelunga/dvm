import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "dvm",
  version = "0.0.1",
  author_email = "dev@doppler.market",
  description = "Doppler Virtual Machine CLI",
  license = "Apache License 2.0",
  long_description=read('README'),
  keywords = "doppler machine learning dvm",
  url = "http://packages.python.org/doppler-dvm",
  packages=['cli', 'tests'],
  install_requires=[
    "requests==2.8.1",
    "cement"
  ],
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Topic :: Utilities",
    "License :: Apache License 2.0"
  ],
  entry_points={
    'console_scripts': [
      'dvm = cli.__main__:main'
    ]
  },
)