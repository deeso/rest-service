#!/usr/bin/env python
from setuptools import setup, find_packages
import os


data_files = [(d, [os.path.join(d, f) for f in files])
              for d, folders, files in os.walk(os.path.join('src', 'config'))]


setup(name='rest-service',
      version='1.0',
      description='boiler plate rest service',
      author='Adam Pridgen',
      author_email='adam.pridgen.phd@gmail.com',
      install_requires=['toml', 'wheel', 'psycopg2', 'Flask-SQLAlchemy', 'quart', 'flask-bcrypt',
                        'flask-wtf', 'flask-restful', 'flask-jwt-extended', 'passlib', 'requests',
                        'quart_openapi', 'jinja', 'pycrypto'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
)
