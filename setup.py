import os
from setuptools import setup, find_packages


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
  packages=[],
  install_requires=[
    "requests",
    "cement",
    "colorlog",
    "jsonmodels",
    "tabulate",
    "flask",
    "persist-queue",
    "tensorflow",
    "keras",
    "scikit-learn>=0.19.0",
    "pandas>=0.20.3",
    "numpy>=1.7.1",
    "h5py"
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