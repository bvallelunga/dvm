import os
from setuptools import setup


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name = "dvm",
  version = "0.0.1",
  author_email = "dev@doppler.market",
  description = "Doppler Virtual Machine CLI",
  license = "Apache License 2.0",
  long_description=read('README.md'),
  keywords = "doppler machine learning dvm",
  url = "http://packages.python.org/doppler-dvm",
  packages=['cli', 'tests'],
  install_requires=[
    "requests==2.8.1",
    "cement",
    "colorlog"
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