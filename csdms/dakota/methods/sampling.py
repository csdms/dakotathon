#! /usr/bin/env python
"""Implementation of the Dakota sampling method."""

from .base import MethodsBase


classname = 'Sampling'


class Sampling(MethodsBase):

    """Define parameters for a Dakota experiment using the sampling method."""

    def __init__(self,
                 variables=('x1', 'x2'),
                 samples=10,
                 sample_type='random',
                 seed=None,
                 lower_bounds=(-1.0, -1.0),
                 upper_bounds=(1.0, 1.0),
                 responses=('y1',),
                 **kwargs):
        """Create a new Dakota sampling study.

        Parameters
        ----------
        variables, responses : array_like of str
          Names used for input and output variables.
        samples: int
          The number of randomly chosen values at which to execute a model.
        sample_type: str
          Technique for choosing samples, `random` or `lhs`.
        seed: int
          The seed for the random number generator.
        lower_bounds, upper_bounds: array_like of float
          Minimum and maximum values of a variable.

        Examples
        --------
        Create a default sampling experiment:

        >>> x = Sampling()

        """
        MethodsBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self.variables = variables
        self._samples = samples
        self._sample_type = sample_type
        self._seed = seed
        self._lower_bounds = lower_bounds
        self._upper_bounds = upper_bounds
        self.responses = responses

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
    def lower_bounds(self):
        """Minimum values of study variables."""
        return self._lower_bounds

    @lower_bounds.setter
    def lower_bounds(self, value):
        """Set minimum values of study variables.

        Parameters
        ----------
        value : list or tuple of numbers
          The minimum values.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Lower bounds must be a tuple or a list")
        self._lower_bounds = value

    @property
    def upper_bounds(self):
        """Maximum values of study variables."""
        return self._upper_bounds

    @upper_bounds.setter
    def upper_bounds(self, value):
        """Set maximum values of study variables.

        Parameters
        ----------
        value : list or tuple of numbers
          The maximum values.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Upper bounds must be a tuple or a list")
        self._upper_bounds = value

    def method_block(self):
        """Define the method block for a sampling experiment.

        See Also
        --------
        csdms.dakota.methods.base.MethodsBase.method_block

        """
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    sample_type = {}\n'.format(self.sample_type) \
            + '    samples = {}\n'.format(self.samples)
        if self.seed is not None:
            s += '    seed = {}\n'.format(self.seed)
        s += '\n'
        return(s)

    def variables_block(self):
        """Define the variables block for a sampling experiment.

        See Also
        --------
        csdms.dakota.methods.base.MethodsBase.variables_block

        """
        s = 'variables\n' \
            + '  {0} = {1}'.format(self.variable_type,
                                   len(self.variables))
        s += '\n' \
             + '    lower_bounds ='
        for b in self.lower_bounds:
            s += ' {}'.format(b)
        s += '\n' \
             + '    upper_bounds ='
        for b in self.upper_bounds:
            s += ' {}'.format(b)
        s += '\n' \
             + '    descriptors ='
        for vd in self.variables:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
