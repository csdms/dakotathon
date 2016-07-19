#! /usr/bin/env python
"""An abstract base class for all Dakota analysis methods."""

from abc import ABCMeta, abstractmethod
import types
import yaml


class MethodsBase(object):

    """Describe features common to all Dakota analysis methods."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, method=None):
        """Create default method parameters.

        Parameters
        ----------
        method : str
          The name of the analysis method; e.g., 'vector_parameter_study'.

        """
        self.method = method

    @classmethod
    def from_file_like(cls, file_like):
        """Create a MethodsBase instance from a file-like object.

        Parameters
        ----------
        file_like : file_like
            Input parameter file.

        Returns
        -------
        MethodsBase
            A new MethodsBase instance.

        """
        config = {}
        if isinstance(file_like, types.StringTypes):
            with open(file_like, 'r') as fp:
                config = yaml.load(fp.read())
        else:
            config = yaml.load(file_like)
        return cls(**config)

    @abstractmethod
    def method_block(self):
        """Define the method block of a Dakota input file."""
        s = 'method\n' \
            + '  {}\n\n'.format(self.method)
        return(s)
