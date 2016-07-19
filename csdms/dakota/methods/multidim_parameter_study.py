#! /usr/bin/env python
"""Implementation of a Dakota multidim parameter study."""

from .base import MethodsBase


classname = 'MultidimParameterStudy'


class MultidimParameterStudy(MethodsBase):

    """Define parameters for a Dakota multidim parameter study."""

    def __init__(self,
                 partitions=(10, 8),
                 **kwargs):
        """Create a new Dakota multidim parameter study.

        Parameters
        ----------
        partitions : array_like of int
          Number of intervals between lower and upper bounds for each study
          parameter.

        Examples
        --------
        Create a default multidim parameter study experiment:

        >>> m = MultidimParameterStudy()

        """
        MethodsBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self._partitions = partitions

    @property
    def partitions(self):
        """The number of evaluation intervals for each parameter."""
        return self._partitions

    @partitions.setter
    def partitions(self, value):
        """Set the number of evaluation intervals for each parameter.

        Parameters
        ----------
        value : list or tuple of int
          The new number of partitions.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Partitions must be a tuple or a list")
        self._partitions = value

    def method_block(self):
        """Define a multidim parameter study method block.

        See Also
        --------
        csdms.dakota.methods.base.MethodsBase.method_block

        """
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    partitions ='
        for p in self.partitions:
            s += ' {}'.format(p)
        s += '\n\n'
        return(s)
