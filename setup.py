#! /usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
from dakota import __version__, plugin_script

setup(name='dakota',
      version=__version__,
      author='Mark Piper',
      author_email='mark.piper@colorado.edu',
      license='MIT',
      description='BMI for Dakota',
      long_description=open('README.md').read(),
      packages=find_packages(exclude=['*.tests']),
      entry_points={
          'console_scripts': [
              plugin_script + ' = dakota.run_plugin:main'
          ]
      }
)
