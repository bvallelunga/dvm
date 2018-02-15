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
    "requests==2.18.4",
    "cement",
    "colorlog==3.1.2",
    "jsonmodels",
    "tabulate==0.8.2",
    "flask==0.12.2",
    "persist-queue==0.2.1",
    "keras==2.1.4",
    "scikit-learn==0.19.1",
    "pandas==0.22.0",
    "numpy==1.12.0",
    #"h5py==2.7.1",
    "torchvision",
    "simplejson==3.13.2"
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
