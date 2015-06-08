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
    def setup(self, config):
        """Configure component inputs.

        Sets attributes using information from the run configuration
        file. The Dakota parsing utility ``dprepro`` reads parameters
        from Dakota to create a new input file from a template.

        Parameters
        ----------
        config : dict
          Stores configuration settings for a Dakota experiment.

        """
        pass

    @abstractmethod
    def call(self):
        """Call the component through the shell."""
        pass

    @abstractmethod
    def load(self, output_file):
        """Read data from a component output file.

        Parameters
        ----------
        output_file : str
          The path to a component output file.

        Returns
        -------
        array_like
          A numpy array, or None on an error.

        """
        pass

    @abstractmethod
    def calculate(self):
        """Calculate Dakota response functions."""
        pass

    @abstractmethod
    def write(self, params_file, results_file):
        """Write a Dakota results file.

        Parameters
        ----------
        params_file : str
          A Dakota parameters file.
        results_file : str
          A Dakota results file.

        """
        pass
