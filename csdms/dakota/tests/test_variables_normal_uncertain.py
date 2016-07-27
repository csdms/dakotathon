"""Tests for the csdms.dakota.variables.normal_uncertain module."""

import os
from nose.tools import raises, assert_true, assert_is_none, assert_equal
from csdms.dakota.variables.normal_uncertain import NormalUncertain


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = NormalUncertain()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether NormalUncertain instantiates."""
    x = NormalUncertain()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_variables():
    """Test the variables attribute."""
    value = c.variables
    assert_equal(value, 'normal_uncertain')


def test_descriptors():
    """Test getting the default descriptors property."""
    value = c.descriptors
    assert_equal(value, ('x1', 'x2'))


def test_get_means():
    """Test getting the means property."""
    assert_equal(c.means, (0.0, 0.0))


def test_set_means():
    """Test setting the means property."""
    for items in [[0,1], (0,1)]:
        c.means = items
        assert_equal(c.means, items)


@raises(TypeError)
def test_set_means_fails_if_scalar():
    """Test that the means property fails with scalar."""
    pt = 42
    c.means = pt


def test_get_std_deviations():
    """Test getting the std_deviations property."""
    assert_equal(c.std_deviations, (1.0, 1.0))


def test_set_std_deviations():
    """Test setting the std_deviations property."""
    for items in [[0,1], (0,1)]:
        c.std_deviations = items
        assert_equal(c.std_deviations, items)


@raises(TypeError)
def test_set_std_deviations_fails_if_scalar():
    """Test that the std_deviations property fails with scalar."""
    pt = 42
    c.std_deviations = pt


def test_get_lower_bounds():
    """Test getting the lower_bounds property."""
    assert_is_none(c.lower_bounds)


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
    assert_is_none(c.upper_bounds)


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


def test_str_length():
    """Test the default length of __str__."""
    x = NormalUncertain()
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 6)
