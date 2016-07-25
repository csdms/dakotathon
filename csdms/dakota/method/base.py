#! /usr/bin/env python
"""An abstract base class for all Dakota analysis methods."""

from abc import ABCMeta, abstractmethod
import types
import yaml


class MethodBase(object):

    """Describe features common to all Dakota analysis methods."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, method=None, **kwargs):
        """Create default method parameters.

        Parameters
        ----------
        method : str
          The name of the analysis method; e.g., 'vector_parameter_study'.

        """
        self.method = method

    def __str__(self):
        """Define the preamble of the Dakota input file method block."""
        s = 'method\n' \
            + '  {}'.format(self.method)
        return(s)
