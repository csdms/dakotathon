"""Tests for the dakotathon.variables.continuous_design module."""

import os
from nose.tools import raises, assert_true, assert_is_none, assert_equal
from dakotathon.variables.continuous_design import ContinuousDesign


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = ContinuousDesign()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether ContinuousDesign instantiates."""
    x = ContinuousDesign()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_variables():
    """Test the variables attribute."""
    value = c.variables
    assert_equal(value, 'continuous_design')


def test_descriptors():
    """Test getting the default descriptors property."""
    value = c.descriptors
    assert_equal(value, ('x1', 'x2'))


def test_get_initial_point():
    """Test getting the initial_point property."""
    assert_equal(c.initial_point, (-0.3, 0.2))


def test_set_initial_point():
    """Test setting the initial_point property."""
    x = ContinuousDesign()
    for items in [[0,1], (0,1)]:
        x.initial_point = items
        assert_equal(x.initial_point, items)


@raises(TypeError)
def test_set_initial_point_fails_if_scalar():
    """Test that the initial_point property fails with scalar."""
    x = ContinuousDesign()
    pt = 42
    x.initial_point = pt


def test_get_lower_bounds():
    """Test getting the lower_bounds property."""
    assert_is_none(c.lower_bounds)


def test_set_lower_bounds():
    """Test setting the lower_bounds property."""
    x = ContinuousDesign()
    for items in [[0,1], (0,1)]:
        x.lower_bounds = items
        assert_equal(x.lower_bounds, items)


@raises(TypeError)
def test_set_lower_bounds_fails_if_scalar():
    """Test that the lower_bounds property fails with scalar."""
    x = ContinuousDesign()
    pt = 42
    x.lower_bounds = pt


def test_get_upper_bounds():
    """Test getting the upper_bounds property."""
    assert_is_none(c.upper_bounds)


def test_set_upper_bounds():
    """Test setting the upper_bounds property."""
    x = ContinuousDesign()
    for items in [[0,1], (0,1)]:
        x.upper_bounds = items
        assert_equal(x.upper_bounds, items)


@raises(TypeError)
def test_set_upper_bounds_fails_if_scalar():
    """Test that the upper_bounds property fails with scalar."""
    x = ContinuousDesign()
    pt = 42
    x.upper_bounds = pt


def test_default_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)


def test_str_length_with_options():
    """Test the length of __str__ with optional props set."""
    x = ContinuousDesign(lower_bounds=(-10, -10), upper_bounds=(10, 10))
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 6)
