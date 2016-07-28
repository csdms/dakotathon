#! /usr/bin/env python
"""Abstract base classes for Dakota analysis methods."""

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
        self._method = method

    @property
    def method(self):
        """The analysis method used in the experiment."""
        return self._method

    @method.setter
    def method(self, value):
        """Set the analysis method used in the experiment.

        Parameters
        ----------
        value : str
          The new method type.

        """
        if not isinstance(value, str):
            raise TypeError("Method must be a str")
        self._method = value

    def __str__(self):
        """Define the preamble of the Dakota input file method block."""
        s = 'method\n' \
            + '  {}'.format(self.method)
        return(s)


class UncertaintyQuantificationBase(MethodBase):

    """Describe features of uncertainty quantification methods."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, basis_polynomial_family='extended', **kwargs):
        """Create default method parameters.

        Parameters
        ----------
        basis_polynomial_family: str, optional
          The type of polynomial basis used in the expansion, either
          'extended' (the default), 'askey', or 'wiener'.

        """
        self._basis_polynomial_family = basis_polynomial_family

    @property
    def basis_polynomial_family(self):
        """The type of basis polynomials used by the method."""
        return self._basis_polynomial_family

    @basis_polynomial_family.setter
    def basis_polynomial_family(self, value):
        """Set the type of basis polynomials used by the method.

        Parameters
        ----------
        value : str
        The polynomial type.

        """
        if value not in ('extended', 'askey', 'wiener'):
            msg = "Polynomial type must be 'extended', 'askey', or 'wiener'"
            raise TypeError(msg)
        self._basis_polynomial_family = value
