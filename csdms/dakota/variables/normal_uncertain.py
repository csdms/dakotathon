"""Implementation of a Dakota normal uncertain variable."""

from .base import VariablesBase


classname = 'NormalUncertain'


class NormalUncertain(VariablesBase):

    """Define attributes for Dakota normal uncertain variables.

    The means and standard deviations are required specifications; the
    initial point, and the distribution lower and upper bounds are
    optional.

    For vector and centered parameter studies, an inferred initial
    starting point is needed for uncertain variables. These variables
    are initialized to their means for these studies.

    """

    def __init__(self,
                 descriptors=('x1', 'x2'),
                 means=(0.0, 0.0),
                 std_deviations=(1.0, 1.0),
                 lower_bounds=None,
                 upper_bounds=None,
                 initial_point=None,
                 **kwargs):
        """Create the parameter set for a normal uncertain variable.

        Parameters
        ----------
        descriptors : str or tuple or list of str, optional
            Labels for the variables.
        means : tuple or list of numbers
            First parameter of Gaussian distribution.
        std_deviations : tuple or list of numbers
            Second parameter of Gaussian distribution.
        lower_bounds : tuple or list of numbers, optional
            Minimum values used by the study variables.
        upper_bounds : tuple or list of numbers, optional
            Maximum values used by the study variables.
        initial_point : tuple or list of numbers, optional
            Start points used by study variables.
        **kwargs
            Optional keyword arguments.

        Examples
        --------
        Create a default instance of NormalUncertain with:

        >>> v = NormalUncertain()
        >>> print v
        variables
          normal_uncertain = 2
            descriptors = 'x1' 'x2'
            means = 0.0 0.0
            std_deviations = 1.0 1.0
        <BLANKLINE>
        <BLANKLINE>
        """
        VariablesBase.__init__(self, **kwargs)
        self.variables = self.__module__.rsplit('.')[-1]
        self._descriptors = descriptors
        self._means = means
        self._std_deviations = std_deviations
        self._lower_bounds = lower_bounds
        self._upper_bounds = upper_bounds
        self._initial_point = initial_point

    @property
    def means(self):
        """Mean values of study variables."""
        return self._means

    @means.setter
    def means(self, value):
        """Set mean values of study variables.

        Parameters
        ----------
        value : list or tuple of numbers
          The mean values.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Means must be a tuple or a list")
        self._means = value

    @property
    def std_deviations(self):
        """Standard deviations of study variables."""
        return self._std_deviations

    @std_deviations.setter
    def std_deviations(self, value):
        """Set standard deviations of study variables.

        Parameters
        ----------
        value : list or tuple of numbers
          The standard deviation values.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Standard deviations must be a tuple or a list")
        self._std_deviations = value

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
        """Define the variables block for a normal uncertain variable.

        See Also
        --------
        csdms.dakota.variables.base.VariablesBase.__str__

        """
        s = VariablesBase.__str__(self)
        if self.means is not None:
            s += '\n' \
                 + '    means ='
            for m in self.means:
                s += ' {}'.format(m)
        if self.std_deviations is not None:
            s += '\n' \
                 + '    std_deviations ='
            for m in self.std_deviations:
                s += ' {}'.format(m)
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
