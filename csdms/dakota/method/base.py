#! /usr/bin/env python
"""Abstract base classes for Dakota analysis methods."""

from abc import ABCMeta, abstractmethod
import types
import yaml


class MethodBase(object):

    """Describe features common to all Dakota analysis methods."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, method='vector_parameter_study', **kwargs):
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
            + '  {}\n'.format(self.method)
        return(s)


def _print_levels(levels):
    s = ''
    for item in levels:
        if isinstance(item, (tuple, list)):
            s += '\n     '
            for subitem in item:
                s += ' {}'.format(subitem)
        else:
            s += ' {}'.format(item)
    s += '\n'
    return s


class UncertaintyQuantificationBase(MethodBase):

    """Describe features of uncertainty quantification methods."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 basis_polynomial_family='extended',
                 probability_levels=(),
                 response_levels=(),
                 samples=10,
                 sample_type='random',
                 seed=None,
                 variance_based_decomp=False,
                 **kwargs):
        """Create default method parameters.

        Parameters
        ----------
        basis_polynomial_family: str, optional
          The type of polynomial basis used in the expansion, either
          'extended' (the default), 'askey', or 'wiener'.
        probability_levels : list or tuple of float, optional
          Specify probability levels at which to estimate the
          corresponding response value.
        response_levels : list or tuple of float, optional
          Values at which to estimate desired statistics for each response
        samples : int
          The number of randomly chosen values at which to execute a model.
        sample_type : str
          Technique for choosing samples, `random` or `lhs`.
        seed : int, optional
          The seed for the random number generator. If seed is
          specified, a stochastic study will generate identical
          results when repeated using the same seed value. If not
          specified, a seed is randomly generated.
        variance_based_decomp : bool, optional
          Set to activate global sensitivity analysis based on
          decomposition of response variance into main, interaction,
          and total effects.

        """
        MethodBase.__init__(self, **kwargs)
        self._basis_polynomial_family = basis_polynomial_family
        self._probability_levels = probability_levels
        self._response_levels = response_levels
        self._samples = samples
        self._sample_type = sample_type
        self._seed = seed
        self._variance_based_decomp = variance_based_decomp

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

    @property
    def probability_levels(self):
        """Probabilities at which to estimate response values."""
        return self._probability_levels

    @probability_levels.setter
    def probability_levels(self, value):
        """Set probabilities at which to estimate response values.

        Parameters
        ----------
        value : tuple or list of float
          The probability levels.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Probability levels must be a tuple or a list")
        self._probability_levels = value

    @property
    def response_levels(self):
        """Values at which to estimate statistics for responses."""
        return self._response_levels

    @response_levels.setter
    def response_levels(self, value):
        """Set values at which to estimate statistics for responses.

        Parameters
        ----------
        value : tuple or list of float
          The response levels.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Response levels must be a tuple or a list")
        self._response_levels = value

    @property
    def samples(self):
        """Number of samples in experiment."""
        return self._samples

    @samples.setter
    def samples(self, value):
        """Set number of samples used in experiment.

        Parameters
        ----------
        value : int
          The number of samples.

        """
        if type(value) is not int:
            raise TypeError("Samples must be an int")
        self._samples = value

    @property
    def sample_type(self):
        """Sampling strategy."""
        return self._sample_type

    @sample_type.setter
    def sample_type(self, value):
        """Set sampling strategy used in experiment.

        Parameters
        ----------
        value : str
          The sampling strategy.

        """
        if ['random', 'lhs'].count(value) == 0:
            raise TypeError("Sample type must be 'random' or 'lhs'")
        self._sample_type = value

    @property
    def seed(self):
        """Seed of the random number generator."""
        return self._seed

    @seed.setter
    def seed(self, value):
        """Set the seed of the random number generator.

        Parameters
        ----------
        value : int
          The random number generator seed.

        """
        if type(value) is not int:
            raise TypeError("Seed must be an int")
        self._seed = value

    @property
    def variance_based_decomp(self):
        """Use variance-based decomposition global sensitivity analysis."""
        return self._variance_based_decomp

    @variance_based_decomp.setter
    def variance_based_decomp(self, value):
        """Toggle variance-based decomposition global sensitivity analysis.

        Parameters
        ----------
        value : bool
          True if using variance-based decomposition.

        """
        if type(value) is not bool:
            raise TypeError("Set variance-based decomposition with a bool")
        self._variance_based_decomp = value

    def __str__(self):
        """Define the method block for a UQ experiment.

        See Also
        --------
        csdms.dakota.method.base.MethodBase.__str__

        """
        s = MethodBase.__str__(self)
        if self.basis_polynomial_family is not 'extended':
            s += '    {}\n'.format(self.basis_polynomial_family)
        s += '    sample_type = {}\n'.format(self.sample_type) \
            + '    samples = {}\n'.format(self.samples)
        if self.seed is not None:
            s += '    seed = {}\n'.format(self.seed)
        if len(self.probability_levels) > 0:
            s += '    probability_levels ='
            s += _print_levels(self.probability_levels)
        if len(self.response_levels) > 0:
            s += '    response_levels ='
            s += _print_levels(self.response_levels)
        if self.variance_based_decomp:
            s += '    variance_based_decomp\n'
        return s
