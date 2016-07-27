"""Implementation of a Dakota uniform uncertain variable."""

from .base import VariablesBase


classname = 'UniformUncertain'


class UniformUncertain(VariablesBase):

    """Define attributes for Dakota uniform uncertain variables."""

    def __init__(self,
                 descriptors=('x1', 'x2'),
                 lower_bounds=(-2.0, -2.0),
                 upper_bounds=(2.0, 2.0),
                 initial_point=None,
                 **kwargs):
        """Create the parameter set for a uniform uncertain variable.

        Parameters
        ----------
        descriptors : str or tuple or list of str, optional
            Labels for the variables.
        initial_point : tuple or list of numbers, optional
            Start points used by study variables.
        lower_bounds : tuple or list of numbers
            Minimum values used by the study variables.
        upper_bounds : tuple or list of numbers
            Maximum values used by the study variables.
        **kwargs
            Optional keyword arguments.

        Examples
        --------
        Create a default instance of UniformUncertain with:

        >>> v = UniformUncertain()
        >>> print v
        variables
          uniform_uncertain = 2
            descriptors = 'x1' 'x2'
            lower_bounds = -2.0 -2.0
            upper_bounds = 2.0 2.0
        <BLANKLINE>
        <BLANKLINE>
        """
        VariablesBase.__init__(self, **kwargs)
        self.variables = self.__module__.rsplit('.')[-1]
        self._descriptors = descriptors
        self._lower_bounds = lower_bounds
        self._upper_bounds = upper_bounds
        self._initial_point = initial_point

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

    def __str__(self):
        """Define the variables block for a uniform uncertain variable.

        See Also
        --------
        csdms.dakota.variables.base.VariablesBase.__str__

        """
        s = VariablesBase.__str__(self)
        if self.lower_bounds is not None:
            s += '\n' \
                 + '    lower_bounds ='
            for b in self.lower_bounds:
                s += ' {}'.format(b)
        if self.upper_bounds is not None:
            s += '\n' \
                 + '    upper_bounds ='
            for b in self.upper_bounds:
                s += ' {}'.format(b)
        if self.initial_point is not None:
            s += '\n' \
                 + '    initial_point ='
            for pt in self.initial_point:
                s += ' {}'.format(pt)
        s += '\n\n'
        return(s)
