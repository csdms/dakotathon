#! /usr/bin/env python
"""Implementation of a Dakota PSUADE MOAT study."""

from .base import MethodBase
from ..utils import to_iterable


classname = 'PsuadeMoatStudy'

class PsuadeMoatStudy(MethodBase):

    """Define parameters for a Dakota PSUADE MOAT study."""

    def __init__(self,
                samples,
                seed,
                partitions=4,
                model_pointer=None,
                 **kwargs):
        """Create a new Dakota PSUADE MOAT study.

        Parameters
        ----------
        samples : array_like of float
          Number of samples.
        seed : int
          Random seed.
        partitions : array_like of int, optional
          Number of partitions (default = 4)
        model_pointer : str, optional
          The id_model of the model block used for the analysis. This should be
          specified if multiple models are being used. If none is specified
          Dakota will use the last model block parsed.
        Examples
        --------
        Create a default centered parameter study experiment:

        >>> c = CenteredParameterStudy()

        """
        MethodBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self._partitions = partitions
        self._model_pointer = model_pointer

        # samples must be r*(num_parameters+1) enforce this here

        self._samples = samples
        self._seed = seed

    @property
    def model_pointer(self):
        """Model pointer name."""
        return self._model_pointer

    @property
    def partitions(self):
        """Number partitions of each parameter dimension."""
        return self._partitions

    @property
    def samples(self):
        """Number of samples."""
        return self._samples

    @property
    def seed(self):
        """Seed value."""
        return self._seed

    def __str__(self):
        """Define a PSUADE MOAT method block.

        See Also
        --------
        dakotathon.method.base.MethodBase.__str__

        """
        s = MethodBase.__str__(self)
        if self._model_pointer is None:
            pass
        else:
            s += '    model_pointer = {} \n'.format(self._model_pointer)
        s += '    partitions = {} \n'.format(self.partitions)
        s += '    samples = {} \n'.format(self.samples)
        s += '    seed = {} \n'.format(self.seed)
        s += '\n\n'
        return(s)
