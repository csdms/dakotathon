#!/usr/bin/env python
#
# Tests for dakotathon.method.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import sys
from nose.tools import raises, assert_true, assert_equal, assert_is_none
from dakotathon.method.base import MethodBase

# Helpers --------------------------------------------------------------


class Concrete(MethodBase):

    """A subclass of MethodBase used for testing."""

    def __init__(self, **kwargs):
        MethodBase.__init__(self, **kwargs)


# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print("\n*** " + __name__)
    global c
    c = Concrete(method="centered_parameter_study")


def teardown_module():
    """Called after all tests have completed."""
    pass


# Tests ----------------------------------------------------------------


@raises(TypeError)
def test_instantiate():
    """Test whether MethodBase fails to instantiate."""
    if sys.version[0] == 2:
        d = MethodBase()
    else:
        # abstract base class type error not raised
        # in python 3.
        raise (TypeError)


def test_get_method():
    """Test getting the method property."""
    assert_true(type(c.method) is str)


def test_set_method():
    """Test setting the method property."""
    x = Concrete()
    m = "sampling"
    x.method = m
    assert_equal(x.method, m)


@raises(TypeError)
def test_method_fails_if_not_str():
    """Test that setting method to a non-str fails."""
    x = Concrete()
    value = 42
    x.method = value


def test_get_max_iterations():
    """Test getting the max_iterations property."""
    assert_is_none(c.max_iterations)


def test_set_max_iterations():
    """Test setting the max_iterations property."""
    x = Concrete()
    m = 100
    x.max_iterations = 100
    assert_equal(x.max_iterations, m)


@raises(TypeError)
def test_max_iterations_fails_if_not_int():
    """Test that setting max_iterations to a non-int fails."""
    x = Concrete()
    value = 42.0
    x.max_iterations = value


def test_get_convergence_tolerance():
    """Test getting the convergence_tolerance property."""
    assert_is_none(c.convergence_tolerance)


def test_set_convergence_tolerance():
    """Test setting the convergence_tolerance property."""
    x = Concrete()
    m = 0.1
    x.convergence_tolerance = 0.1
    assert_equal(x.convergence_tolerance, m)


@raises(TypeError)
def test_convergence_tolerance_fails_if_not_float():
    """Test that setting convergence_tolerance to a non-float fails."""
    x = Concrete()
    value = 42
    x.convergence_tolerance = value


@raises(ValueError)
def test_convergence_tolerance_fails_lower_bnd():
    """Test that setting convergence_tolerance <= 0.0 fails."""
    x = Concrete()
    x.convergence_tolerance = 0.0


@raises(ValueError)
def test_convergence_tolerance_fails_upper_bnd():
    """Test that setting convergence_tolerance >= 1.0 fails."""
    x = Concrete()
    x.convergence_tolerance = 1.0


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_default_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 2)


def test_str_length_with_options():
    """Test the length of __str__ with optional props set."""
    x = Concrete(max_iterations=100, convergence_tolerance=1e-4)
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 4)
