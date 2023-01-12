#!/usr/bin/env python

from distutils.core import setup

setup(name="teaching-platform",
      version="0.1.0",
      packages=["teaching-platform"],
      install_requires = ["pyyaml","password_strength", "flask","flask_sqlalchemy", "jsonpickle"]
      )