from distutils.core import setup
from setuptools import find_packages

import nhlscrapi

setup(
  name="nhlscrapi",
    
  version=nhlscrapi.__version__,
    
  description='NHL Scrapr API for Python',
  long_description=open('README.rst').read(),
    
  author='Rob Howley',
  author_email='howley.robert@gmail.com',
  url='https://github.com/robhowley/nhlscrapi',
    
  packages=find_packages(),
    
  include_package_data=True,
    
  scripts=['bin/gamedata.py'],
    
  license="Apache Software License version 2.0",
    
  platforms='any',
    
  zip_safe=False,
    
  keywords='nhlscrapi',
    
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
    
  test_suite='tests',
    
  # Dependent packages (distributions)
  install_requires=['lxml']
)
