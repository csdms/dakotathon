#! /usr/bin/env python
"""Implementation of a Dakota vector parameter study."""

from .base import MethodsBase


classname = 'VectorParameterStudy'


class VectorParameterStudy(MethodsBase):

    """Define parameters for a Dakota vector parameter study."""

    def __init__(self,
                 variables=('x1', 'x2'),
                 initial_point=(-0.3, 0.2),
                 final_point=(1.1, 1.3),
                 n_steps=10,
                 response_descriptors=('y1',),
                 **kwargs):
        """Create a new Dakota vector parameter study.

        Parameters
        ----------
        variables, response_descriptors : array_like of str
          Names used for input and output variables.
        initial_point : array_like of float
          Start point for the parameter study.
        final_point : array_like of float
          End point for the parameter study.
        n_steps : int
          Number of steps along vector.

        Examples
        --------
        Create a default vector parameter study experiment:

        >>> v = VectorParameterStudy()

        """
        MethodsBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self.variables = variables
        self._initial_point = initial_point
        self._final_point = final_point
        self.n_steps = n_steps
        self.response_descriptors = response_descriptors

    @property
    def initial_point(self):
        """Start points used by study variables."""
        return self._initial_point

    @initial_point.setter
    def initial_point(self, value):
        """Set start points used by study variables.

        Parameters
        ----------
        value : list or tuple of numbers
          The new initial points.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Initial points must be a tuple or a list")
        self._initial_point = value

    @property
    def final_point(self):
        """End points used by study variables."""
        return self._final_point

    @final_point.setter
    def final_point(self, value):
        """Set end points used by study variables.

        Parameters
        ----------
        value : list or tuple of numbers
          The new final points.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Final points must be a tuple or a list")
        self._final_point = value

    def method_block(self):
        """Define a vector parameter study method block for a Dakota input file.

        See Also
        --------
        csdms.dakota.methods.base.MethodsBase.method_block

        """
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    final_point ='
        for pt in self.final_point:
            s += ' {}'.format(pt)
        s += '\n' \
            + '    num_steps = {}\n\n'.format(self.n_steps)
        return(s)

    def variables_block(self):
        """Define a vector parameter study variables block for a Dakota input file.

        See Also
        --------
        csdms.dakota.methods.base.MethodsBase.variables_block

        """
        s = 'variables\n' \
            + '  {0} = {1}\n'.format(self.variable_type,
                                     len(self.variables)) \
            + '    initial_point ='
        for pt in self.initial_point:
            s += ' {}'.format(pt)
        s += '\n' \
             + '    descriptors ='
        for vd in self.variables:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
