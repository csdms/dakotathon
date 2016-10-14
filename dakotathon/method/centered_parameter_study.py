#! /usr/bin/env python
"""Implementation of a Dakota centered parameter study."""

from .base import MethodBase


classname = 'CenteredParameterStudy'


class CenteredParameterStudy(MethodBase):

    """Define parameters for a Dakota centered parameter study."""

    def __init__(self,
                 steps_per_variable=(5, 4),
                 step_vector=(0.4, 0.5),
                 **kwargs):
        """Create a new Dakota centered parameter study.

        Parameters
        ----------
        steps_per_variable : array_like of int
          Number of steps to take in each direction.
        steps_vector : array_like of float
          Size of steps in each direction.

        Examples
        --------
        Create a default centered parameter study experiment:

        >>> c = CenteredParameterStudy()

        """
        MethodBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self._steps_per_variable = steps_per_variable
        self._step_vector = step_vector

    @property
    def steps_per_variable(self):
        """Number of steps to take in each direction."""
        return self._steps_per_variable

    @steps_per_variable.setter
    def steps_per_variable(self, value):
        """Set number of steps to take in each direction.

        Parameters
        ----------
        value : list or tuple of int
          The new number of steps.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Steps must be a tuple or a list")
        self._steps_per_variable = value

    @property
    def step_vector(self):
        """Step size in each direction."""
        return self._step_vector

    @step_vector.setter
    def step_vector(self, value):
        """Set step size in each direction.

        Parameters
        ----------
        value : list or tuple of int
          The new step size.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Step size must be a tuple or a list")
        self._step_vector = value

    def __str__(self):
        """Define a centered parameter study method block.

        See Also
        --------
        dakotathon.method.base.MethodBase.__str__

        """
        s = MethodBase.__str__(self)
        s += '    steps_per_variable ='
        for step in self.steps_per_variable:
            s += ' {}'.format(step)
        s += '\n' \
            + '    step_vector ='
        for step in self.step_vector:
            s += ' {}'.format(step)
        s += '\n\n'
        return(s)
