#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name="teaching_platform",
      version="0.1.0",
      packages=find_packages(),
      install_requires = ["pyyaml", "flask", "jsonpickle","python-dotenv", "flask_socketio",
                          "password_strength", "flask_sqlalchemy","flask_httpauth"]
      )