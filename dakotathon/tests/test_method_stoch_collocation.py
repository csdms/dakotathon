"""Tests for the csdms.dakota.method.stoch_collocation module."""

from nose.tools import (raises, assert_is_instance, assert_true,
                        assert_equal, assert_is_none)
from csdms.dakota.method.stoch_collocation import StochasticCollocation


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global x
    x = StochasticCollocation()


def teardown_module():
    """Called after all tests have completed."""
    pass


def test_init_no_params():
    """Test creating an instance with no parameters."""
    x1 = StochasticCollocation()
    assert_is_instance(x1, StochasticCollocation)


def test_method_attr():
    """Test the value of the method attribute."""
    assert_equal(x.method, 'stoch_collocation')


def test_get_basis_polynomial_family():
    """Test getting the basis_polynomial_family property."""
    assert_true(type(x.basis_polynomial_family) is str)


def test_set_basis_polynomial_family():
    """Test setting the basis_polynomial_family property."""
    m = StochasticCollocation()
    p = 'piecewise'
    m.basis_polynomial_family = p
    assert_equal(m.basis_polynomial_family, p)


@raises(TypeError)
def test_basis_polynomial_family_fails_if_unknown_type():
    """Test that setting basis_polynomial_family to an unknown type fails."""
    value = 'foobar'
    x.basis_polynomial_family = value


def test_get_quadrature_order():
    """Test getting the quadrature_order property."""
    assert_true(type(x.quadrature_order) is int)


def test_set_quadrature_order():
    """Test setting the quadrature_order property."""
    m = StochasticCollocation()
    quadrature_order = 42
    m.quadrature_order = quadrature_order
    assert_equal(m.quadrature_order, quadrature_order)


@raises(TypeError)
def test_set_quadrature_order_fails_if_float():
    """Test that the quadrature_order property fails with a float."""
    m = StochasticCollocation()
    quadrature_order = 42.0
    m.quadrature_order = quadrature_order


def test_get_dimension_preference():
    """Test getting the dimension_preference property."""
    assert_true(type(x.dimension_preference) is tuple)


def test_set_dimension_preference():
    """Test setting the dimension_preference property."""
    m = StochasticCollocation()
    for items in [[0,1], (0,1)]:
        m.dimension_preference = items
        assert_equal(m.dimension_preference, items)


@raises(TypeError)
def test_set_dimension_preference_fails_if_scalar():
    """Test that the dimension_preference property fails with scalar."""
    m = StochasticCollocation()
    pt = 42
    m.dimension_preference = pt


def test_dimension_preference_sets_quadrature_order1():
    """Test that dimension_preference sets quadrature order."""
    m = StochasticCollocation()
    m.dimension_preference = [3, 4, 5]
    assert_equal(m.quadrature_order, max(m.dimension_preference))


def test_dimension_preference_sets_quadrature_order2():
    """Test that dimension_preference sets quadrature order."""
    m = StochasticCollocation(dimension_preference=[3, 4, 5])
    assert_equal(m.quadrature_order, max(m.dimension_preference))


def test_dimension_preference_sets_quadrature_order3():
    """Test that dimension_preference sets quadrature order."""
    m = StochasticCollocation(dimension_preference=[3, 4, 5])
    m.quadrature_order=42
    assert_equal(m.quadrature_order, max(m.dimension_preference))


def test_get_nested():
    """Test getting the nested property."""
    assert_true(type(x.nested) is bool)


def test_set_nested():
    """Test setting the nested property."""
    m = StochasticCollocation()
    nested = True
    m.nested = nested
    assert_equal(m.nested, nested)


@raises(TypeError)
def test_set_nested_fails_if_float():
    """Test that the nested property fails with a float."""
    m = StochasticCollocation()
    nested = 42.0
    m.nested = nested


def test_str_special():
    """Test type of __str__ method results."""
    s = str(x)
    assert_true(type(s) is str)


def test_default_str_length():
    """Test the default length of __str__."""
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 7)


def test_str_length_with_options():
    """Test the length of __str__ with optional props set."""
    m = StochasticCollocation(dimension_preference=(1, 2), nested=True)
    s = str(m)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 8)
