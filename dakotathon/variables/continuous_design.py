"""Implementation of a Dakota continous design variable."""

from .base import VariablesBase
from ..utils import to_iterable


classname = 'ContinuousDesign'


class ContinuousDesign(VariablesBase):

    """Define attributes for Dakota continous design variables.

    Continuous variables are defined by a real interval and are
    changed during the search for the optimal design.

    """

    def __init__(self,
                 descriptors=('x1', 'x2'),
                 initial_point=None,
                 lower_bounds=None,
                 upper_bounds=None,
                 **kwargs):
        """Create the parameter set for a continuous design variable.

        Parameters
        ----------
        descriptors : str or tuple or list of str, optional
            Labels for the variables.
        initial_point : tuple or list of numbers
            Start points used by study variables.
        lower_bounds : tuple or list of numbers
            Minimum values used by the study variables.
        upper_bounds : tuple or list of numbers
            Maximum values used by the study variables.
        **kwargs
            Optional keyword arguments.

        Examples
        --------
        Create a default ContinuousDesign instance with:

        >>> v = ContinuousDesign()

        """
        VariablesBase.__init__(self, **kwargs)
        self.variables = self.__module__.rsplit('.')[-1]
        self._descriptors = descriptors
        self._initial_point = initial_point
        self._lower_bounds = lower_bounds
        self._upper_bounds = upper_bounds

        if initial_point is None and lower_bounds is None and \
            upper_bounds is None: self._initial_point = (-0.3, 0.2)

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

    def __str__(self):
        """Define the variables block for continous design variables.

        Examples
        --------
        Display the variables block created by a default instance of
        ContinuousDesign:

        >>> v = ContinuousDesign()
        >>> print v
        variables
          continuous_design = 2
            descriptors = 'x1' 'x2'
            initial_point = -0.3 0.2
        <BLANKLINE>
        <BLANKLINE>

        See Also
        --------
        dakotathon.variables.base.VariablesBase.__str__

        """
        s = VariablesBase.__str__(self)
        if self.initial_point is not None:
            initial_point = to_iterable(self.initial_point)
            s += '\n' \
                 + '    initial_point ='
            for pt in initial_point:
                s += ' {}'.format(pt)
        if self.lower_bounds is not None:
            lower_bounds = to_iterable(self.lower_bounds)
            s += '\n' \
                 + '    lower_bounds ='
            for b in lower_bounds:
                s += ' {}'.format(b)
        if self.upper_bounds is not None:
            upper_bounds = to_iterable(self.upper_bounds)
            s += '\n' \
                 + '    upper_bounds ='
            for b in upper_bounds:
                s += ' {}'.format(b)
        s += '\n\n'
        return(s)
