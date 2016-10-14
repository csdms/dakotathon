from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
from dakotathon import __version__
from dakotathon.run_plugin import plugin_script


setup(name='dakotathon',
      version=__version__,
      author='Mark Piper',
      author_email='mark.piper@colorado.edu',
      license='MIT',
      description='A Python API for the Dakota systems analysis toolkit',
      long_description=open('README.md').read(),
      install_requires=[
          'numpy',
          'pyyaml',
          'nose',
          'basic-modeling-interface',
      ],
      packages=find_packages(exclude=['*.tests']),
      entry_points={
          'console_scripts': [
              plugin_script + ' = csdms.dakota.run_plugin:main'
          ]
      },
      keywords='CSDMS Dakota uncertainty sensitivity model modeling',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
)
