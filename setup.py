#!/usr/bin/env python3

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
  packages=find_packages(exclude=["tests", "templates", "experiments"]),
  install_requires=[
    "requests",
    "cement",
    "colorlog",
    "jsonmodels",
    "tabulate",
    "flask",
    "persist-queue",
    "keras",
    "scikit-learn",
    "scipy",
    "pandas",
    "numpy",
    "torchvision",
    "simplejson"
  ],
  dependency_links=[
    "pip3 install http://download.pytorch.org/whl/cu91/torch-0.3.1-cp35-cp35m-linux_x86_64.whl",
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
