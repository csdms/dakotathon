"""Implementation of a Dakota continous design variable."""

from .base import VariableBase


classname = 'ContinuousDesign'


class ContinuousDesign(VariableBase):

    """Define attributes for Dakota continous design variables."""

    def __init__(self,
                 descriptors=('x1', 'x2'),
                 initial_point=None,
                 lower_bounds=None,
                 upper_bounds=None,
                 scale_types=None,
                 scales=None,
                 **kwargs):
        VariableBase.__init__(self, **kwargs)
        self.variables = self.__module__.rsplit('.')[-1]
        self._descriptors = descriptors
        self._initial_point = initial_point
        self._lower_bounds = lower_bounds
        self._upper_bounds = upper_bounds

        if initial_point is None and lower_bounds is None and \
            upper_bounds is None: self._initial_point = (0.0, 0.0)

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

    def variables_block(self):
        """Define the variables block for continous design variables."""
        s = 'variables\n'
        s += '  {0} = {1}'.format(self.variables,
                                   len(self.descriptors))
        if self.initial_point is not None:
            s += '\n' \
                 + '    initial_point ='
            for pt in self.initial_point:
                s += ' {}'.format(pt)
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
        s += '\n' \
             + '    descriptors ='
        for vd in self.descriptors:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
