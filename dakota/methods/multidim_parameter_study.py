#! /usr/bin/env python
"""Implementation of a Dakota multidim parameter study."""

from .base import DakotaBase


classname = 'MultidimParameterStudy'


class MultidimParameterStudy(DakotaBase):

    """Define parameters for a Dakota multidim parameter study."""

    def __init__(self,
                 variable_descriptors=('x1', 'x2'),
                 lower_bounds=(-2.0, -2.0),
                 upper_bounds=(2.0, 2.0),
                 partitions=(10, 8),
                 response_descriptors=('y1',),
                 **kwargs):
        """Create a new Dakota multidim parameter study.

        Parameters
        ----------
        variable_descriptors, response_descriptors : array_like of str
          Names used for input and output variables.
        lower_bounds : array_like of float
          Minimum allowable parameter values.
        upper_bounds : array_like of float
          Maximum allowable parameter values.
        partitions : array_like of int
          Number of intervals between lower and upper bounds for each study
          parameter.

        Examples
        --------
        Create a default multidim parameter study experiment:

        >>> m = MultidimParameterStudy()

        """
        DakotaBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self.variable_descriptors = variable_descriptors
        self._lower_bounds = lower_bounds
        self._upper_bounds = upper_bounds
        self._partitions = partitions
        self.response_descriptors = response_descriptors

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
          The new lower bounds.

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
          The new upper bounds.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Upper bounds must be a tuple or a list")
        self._upper_bounds = value

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
        dakota.methods.base.DakotaBase.method_block

        """
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    partitions ='
        for p in self.partitions:
            s += ' {}'.format(p)
        s += '\n\n'
        return(s)

    def variables_block(self):
        """Define a multidim parameter study variables block.

        See Also
        --------
        dakota.methods.base.DakotaBase.variables_block

        """
        s = 'variables\n' \
            + '  {0} = {1}\n'.format(self.variable_type,
                                     len(self.variable_descriptors)) \
            + '    lower_bounds ='
        for b_lo in self.lower_bounds:
            s += ' {}'.format(b_lo)
        s += '\n' \
             + '    upper_bounds ='
        for b_hi in self.upper_bounds:
            s += ' {}'.format(b_hi)
        s += '\n' \
             + '    descriptors ='
        for vd in self.variable_descriptors:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
