#! /usr/bin/env python
"""Implementation of the Dakota sampling method."""

from .base import MethodBase


classname = 'Sampling'


class Sampling(MethodBase):

    """Define parameters for a Dakota experiment using the sampling method."""

    def __init__(self,
                 samples=10,
                 sample_type='random',
                 seed=None,
                 **kwargs):
        """Create a new Dakota sampling study.

        Parameters
        ----------
        samples: int
          The number of randomly chosen values at which to execute a model.
        sample_type: str
          Technique for choosing samples, `random` or `lhs`.
        seed: int
          The seed for the random number generator.

        Examples
        --------
        Create a default sampling experiment:

        >>> x = Sampling()

        """
        MethodBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self._samples = samples
        self._sample_type = sample_type
        self._seed = seed

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

    def __str__(self):
        """Define the method block for a sampling experiment.

        See Also
        --------
        csdms.dakota.method.base.MethodBase.__str__

        """
        s = MethodBase.__str__(self)
        s += '\n' \
             + '    sample_type = {}\n'.format(self.sample_type) \
             + '    samples = {}\n'.format(self.samples)
        if self.seed is not None:
            s += '    seed = {}\n'.format(self.seed)
        s += '\n'
        return(s)
