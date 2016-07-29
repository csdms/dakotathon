#! /usr/bin/env python
"""Implementation of the Dakota polynomial chaos method."""

from .base import UncertaintyQuantificationBase


classname = 'PolynomialChaos'


def _print_levels(levels):
    s = ''
    for item in levels:
        if isinstance(item, (tuple, list)):
            s += '\n     '
            for subitem in item:
                s += ' {}'.format(subitem)
        else:
            s += ' {}'.format(item)
    s += '\n'
    return s


class PolynomialChaos(UncertaintyQuantificationBase):

    """The Dakota polynomial chaos analysis method.

    Designation of a coefficient estimation approach is required, but
    the only approach currently implemented is
    *quadrature_order_sequence*, which obtains coefficients of the
    expansion using multidimensional integration by a tensor-product
    of Gaussian quadrature rules specified with *quadrature_order*,
    and, optionally, with *dimension_preference*. If
    *dimension_preference* is defined, its highest value is set to the
    *quadrature_order*.

    To supply *probability_levels* or *response_levels* to multiple
    responses, nest the inputs to these properties.

    Notes
    -----
    This implementation of the polynomial chaos method is based on the
    `Dakota 6.4 documentation`_.

    .. _Dakota 6.4 documentation:
       https://dakota.sandia.gov//sites/default/files/docs/6.4/html-ref/method-polynomial_chaos.html

    """

    def __init__(self,
                 coefficient_estimation_approach='quadrature_order_sequence',
                 quadrature_order=2,
                 dimension_preference=(),
                 nested=False,
                 probability_levels=(),
                 response_levels=(),
                 samples=10,
                 sample_type='random',
                 seed=None,
                 variance_based_decomp=False,
                 **kwargs):
        """Create a new Dakota sampling study.

        Parameters
        ----------
        coefficient_estimation_approach : str
          Technique to obtain coefficients of expansion.
        quadrature_order : int
          The highest order of the polynomial basis.
        dimension_preference : list or tuple of int, optional
          A set of weights specifying the relative importance of each
          uncertain variable (dimension).
        nested : bool, optional
          Set to enforce nested quadrature rules, if available (default is False).
        probability_levels : list or tuple of float, optional
          Specify probability levels at which to estimate the
          corresponding response value.
        response_levels : list or tuple of float, optional
          Values at which to estimate desired statistics for each response
        samples : int
          The number of randomly chosen values at which to execute a model.
        sample_type : str
          Technique for choosing samples, `random` or `lhs`.
        seed : int, optional
          The seed for the random number generator. If seed is
          specified, a stochastic study will generate identical
          results when repeated using the same seed value. If not
          specified, a seed is randomly generated.

        Examples
        --------
        Create a default instance of PolynomialChaos with:

        >>> m = PolynomialChaos()

        """
        UncertaintyQuantificationBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self.coefficient_estimation_approach = coefficient_estimation_approach
        self._quadrature_order = quadrature_order
        self._dimension_preference = dimension_preference
        self._nested = nested
        self._probability_levels = probability_levels
        self._response_levels = response_levels
        self._samples = samples
        self._sample_type = sample_type
        self._seed = seed

        if len(self.dimension_preference) > 0:
            self.quadrature_order = max(self.dimension_preference)

    @property
    def quadrature_order(self):
        """The highest order polynomial used by the method."""
        return self._quadrature_order

    @quadrature_order.setter
    def quadrature_order(self, value):
        """Set the highest order polynomial used by the method.

        Parameters
        ----------
        value : int
          The polynomial order.

        """
        if type(value) is not int:
            raise TypeError("Quadrature order must be an int")
        if len(self._dimension_preference) > 0:
            self._quadrature_order = max(self._dimension_preference)
        else:
            self._quadrature_order = value

    @property
    def dimension_preference(self):
        """Weights specifying the relative importance of each dimension."""
        return self._dimension_preference

    @dimension_preference.setter
    def dimension_preference(self, value):
        """Set weights specifying the relative importance of each dimension.

        The highest value of dimension_preference is set as the
        quadrature_order.

        Parameters
        ----------
        value : tuple or list of int
          The weights.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Dimension preference must be a tuple or a list")
        self._dimension_preference = value
        self.quadrature_order = max(self.dimension_preference)

    @property
    def nested(self):
        """Enforce use of nested quadrature rules."""
        return self._nested

    @nested.setter
    def nested(self, value):
        """Toggle use of nested quadrature rules.

        Parameters
        ----------
        value : bool
          True if nested.

        """
        if type(value) is not bool:
            raise TypeError("Nested must be a bool")
        self._nested = value

    @property
    def probability_levels(self):
        """Probabilities at which to estimate response values."""
        return self._probability_levels

    @probability_levels.setter
    def probability_levels(self, value):
        """Set probabilities at which to estimate response values.

        Parameters
        ----------
        value : tuple or list of float
          The probability levels.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Probability levels must be a tuple or a list")
        self._probability_levels = value

    @property
    def response_levels(self):
        """Values at which to estimate statistics for responses."""
        return self._response_levels

    @response_levels.setter
    def response_levels(self, value):
        """Set values at which to estimate statistics for responses.

        Parameters
        ----------
        value : tuple or list of float
          The response levels.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Response levels must be a tuple or a list")
        self._response_levels = value

    @property
    def samples(self):
        """Number of samples in experiment."""
        return self._samples

    @samples.setter
    def samples(self, value):
        """Set number of samples used in experiment.

        Parameters
        ----------
        value : int
          The number of samples.

        """
        if type(value) is not int:
            raise TypeError("Samples must be an int")
        self._samples = value

    @property
    def sample_type(self):
        """Sampling strategy."""
        return self._sample_type

    @sample_type.setter
    def sample_type(self, value):
        """Set sampling strategy used in experiment.

        Parameters
        ----------
        value : str
          The sampling strategy.

        """
        if ['random', 'lhs'].count(value) == 0:
            raise TypeError("Sample type must be 'random' or 'lhs'")
        self._sample_type = value

    @property
    def seed(self):
        """Seed of the random number generator."""
        return self._seed

    @seed.setter
    def seed(self, value):
        """Set the seed of the random number generator.

        Parameters
        ----------
        value : int
          The random number generator seed.

        """
        if type(value) is not int:
            raise TypeError("Seed must be an int")
        self._seed = value

    def __str__(self):
        """Define the method block for a polynomial_chaos experiment.

        Examples
        --------
        Display the method block created by a default instance of
        PolynomialChaos:

        >>> m = PolynomialChaos()
        >>> print m
        method
          polynomial_chaos
            quadrature_order = 2
            non_nested
            sample_type = random
            samples = 10
        <BLANKLINE>
        <BLANKLINE>

        See Also
        --------
        csdms.dakota.method.base.UncertaintyQuantificationBase.__str__

        """
        s = UncertaintyQuantificationBase.__str__(self)
        if self.coefficient_estimation_approach == 'quadrature_order_sequence':
            s += '    quadrature_order = {}\n'.format(self.quadrature_order)
            if len(self.dimension_preference) > 0:
                s += '    dimension_preference ='
                for item in self.dimension_preference:
                    s += ' {}'.format(item)
                s += '\n'
            if self.nested:
                s += '    nested\n'
            else:
                s += '    non_nested\n'
        if len(self.probability_levels) > 0:
            s += '    probability_levels ='
            s += _print_levels(self.probability_levels)
        if len(self.response_levels) > 0:
            s += '    response_levels ='
            s += _print_levels(self.response_levels)
        s += '    sample_type = {}\n'.format(self.sample_type) \
            + '    samples = {}\n'.format(self.samples)
        if self.seed is not None:
            s += '    seed = {}\n'.format(self.seed)
        s += '\n'
        return(s)
