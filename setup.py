from setuptools import setup, find_packages
from dakotathon import __version__
from dakotathon.run_plugin import plugin_script
from dakotathon.run_component import component_script


def read_requirements():
    import os

    path = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(path, "requirements.txt")
    try:
        with open(requirements_file, "r") as req_fp:
            requires = req_fp.read().split()
    except IOError:
        return []
    else:
        return [require.split() for require in requires]


setup(
    name="dakotathon",
    version=__version__,
    author="Mark Piper",
    author_email="mark.piper@colorado.edu",
    license="MIT",
    description="A Python API for the Dakota systems analysis toolkit",
    long_description=open("README.md").read(),
    setup_requires=["setuptools"],
    packages=find_packages(exclude=["*.tests"]),
    entry_points={
        "console_scripts": [
            plugin_script + " = dakotathon.run_plugin:main",
            component_script + " = dakotathon.run_component:main",
        ]
    },
    keywords="CSDMS Dakota uncertainty sensitivity model modeling",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
