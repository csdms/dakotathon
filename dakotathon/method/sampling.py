#! /usr/bin/env python
"""Implementation of the Dakota sampling method."""

from .base import UncertaintyQuantificationBase


classname = 'Sampling'


class Sampling(UncertaintyQuantificationBase):

    """The Dakota sampling method."""

    def __init__(self, **kwargs):
        """Create a new Dakota sampling study.

        Examples
        --------
        Create a default sampling experiment:

        >>> x = Sampling()

        """
        UncertaintyQuantificationBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]

    def __str__(self):
        """Define the method block for a sampling experiment.

        See Also
        --------
        dakotathon.method.base.UncertaintyQuantificationBase.__str__

        """
        s = UncertaintyQuantificationBase.__str__(self)
        s += '\n'
        return(s)
