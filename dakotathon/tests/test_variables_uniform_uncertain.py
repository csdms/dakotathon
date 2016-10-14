"""Tests for the csdms.dakota.variables.uniform_uncertain module."""

import os
from nose.tools import raises, assert_true, assert_is_none, assert_equal
from csdms.dakota.variables.uniform_uncertain import UniformUncertain


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = UniformUncertain()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether UniformUncertain instantiates."""
    x = UniformUncertain()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_variables():
    """Test the variables attribute."""
    value = c.variables
    assert_equal(value, 'uniform_uncertain')


def test_descriptors():
    """Test getting the default descriptors property."""
    value = c.descriptors
    assert_equal(value, ('x1', 'x2'))


def test_get_initial_point():
    """Test getting the initial_point property."""
    assert_is_none(c.initial_point)


def test_set_initial_point():
    """Test setting the initial_point property."""
    for items in [[0,1], (0,1)]:
        c.initial_point = items
        assert_equal(c.initial_point, items)


@raises(TypeError)
def test_set_initial_point_fails_if_scalar():
    """Test that the initial_point property fails with scalar."""
    pt = 42
    c.initial_point = pt


def test_get_lower_bounds():
    """Test getting the lower_bounds property."""
    assert_equal(c.lower_bounds, (-2.0, -2.0))


def test_set_lower_bounds():
    """Test setting the lower_bounds property."""
    for items in [[0,1], (0,1)]:
        c.lower_bounds = items
        assert_equal(c.lower_bounds, items)


@raises(TypeError)
def test_set_lower_bounds_fails_if_scalar():
    """Test that the lower_bounds property fails with scalar."""
    pt = 42
    c.lower_bounds = pt


def test_get_upper_bounds():
    """Test getting the upper_bounds property."""
    assert_equal(c.upper_bounds, (2.0, 2.0))


def test_set_upper_bounds():
    """Test setting the upper_bounds property."""
    for items in [[0,1], (0,1)]:
        c.upper_bounds = items
        assert_equal(c.upper_bounds, items)


@raises(TypeError)
def test_set_upper_bounds_fails_if_scalar():
    """Test that the upper_bounds property fails with scalar."""
    pt = 42
    c.upper_bounds = pt


def test_default_str_length():
    """Test the default length of __str__."""
    x = UniformUncertain()
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 6)


def test_str_length_with_options():
    """Test the length of __str__ with optional props set."""
    x = UniformUncertain(initial_point=(0.0, 0.0))
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 7)
