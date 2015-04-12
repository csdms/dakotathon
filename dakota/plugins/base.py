#! /usr/bin/env python
"""An abstract base class for all Dakota component plugins."""

from abc import ABCMeta, abstractmethod


class PluginBase(object):

    """Describe features common to all Dakota plugins."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        """Define default attributes."""
        pass

    @abstractmethod
    def setup(self):
        """Configure component inputs."""
        pass

    @abstractmethod
    def call(self):
        """Call the component through the shell."""
        pass

    @abstractmethod
    def load(self):
        """Read data from a component output file."""
        pass

    @abstractmethod
    def calculate(self):
        """Calculate Dakota response functions."""
        pass

    @abstractmethod
    def write(self):
        """Write a Dakota results file."""
        pass
