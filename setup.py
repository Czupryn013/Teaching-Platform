#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name="tp_models",
      version="0.1.0",
      packages=find_packages(),
      install_requires = ["pyyaml","password_strength", "flask","flask_sqlalchemy", "jsonpickle", "flask_httpauth",
                          "psycopg2", "flask_mail","python-dotenv"]
      )