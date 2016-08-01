#! /usr/bin/env python
"""Implementation of the Dakota stochastic collocation method."""

from .base import UncertaintyQuantificationBase


classname = 'StochasticCollocation'


class StochasticCollocation(UncertaintyQuantificationBase):

    """The Dakota stochastic collocation uncertainty quantification method.

    Stochastic collocation is a general framework for approximate
    representation of random response functions in terms of
    finite-dimensional interpolation bases. Stochastic collocation is
    very similar to polynomial chaos, with the key difference that the
    orthogonal polynomial basis functions are replaced with
    interpolation polynomial bases.

    Notes
    -----
    This implementation of the stochastic collocation method is based
    on the description provided in the `Dakota 6.4 documentation`_.

    .. _Dakota 6.4 documentation:
       https://dakota.sandia.gov//sites/default/files/docs/6.4/html-ref/method-stoch_collocation.html

    """

    def __init__(self,
                 # automated_refinement_type=None,
                 # refinement_type=None,
                 coefficient_estimation_approach='quadrature_order_sequence',
                 quadrature_order=2,
                 dimension_preference=(),
                 nested=False,
                 **kwargs):
        """Create a new Dakota stochastic collocation study.

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

        Examples
        --------
        Create a default instance of StochasticCollocation with:

        >>> m = StochasticCollocation()

        """
        UncertaintyQuantificationBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit('.')[-1]
        self._automated_refinement_type = automated_refinement_type
        self._refinement_type = refinement_type
        self.coefficient_estimation_approach = coefficient_estimation_approach
        self._quadrature_order = quadrature_order
        self._dimension_preference = dimension_preference
        self._nested = nested

        if len(self.dimension_preference) > 0:
            self.quadrature_order = max(self.dimension_preference)

        # if self.automated_refinement_type is not None:
        #     if self.refinement_type is None:
        #         self.refinement_type = 'uniform'
        #     if self.max_iterations is None:
        #         self.max_iterations = 100
        #     if self.convergence_tolerance is None:
        #         self.convergence_tolerance = 1e-4

    @UncertaintyQuantificationBase.basis_polynomial_family.setter
    def basis_polynomial_family(self, value):
        """Set the type of basis polynomials used by the method.

        Parameters
        ----------
        value : str
        The polynomial type.

        """
        if value not in ('extended', 'askey', 'wiener', 'piecewise'):
            msg = 'Polynomial type must be extended, askey, ' \
                  + 'piecewise, or wiener'
            raise TypeError(msg)
        self._basis_polynomial_family = value

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

    def __str__(self):
        """Define the method block for a stoch_collocation experiment.

        Examples
        --------
        Display the method block created by a default instance of
        StochasticCollocation:

        >>> m = StochasticCollocation()
        >>> print m
        method
          stoch_collocation
            sample_type = random
            samples = 10
            quadrature_order = 2
            non_nested
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
        s += '\n'
        return(s)
