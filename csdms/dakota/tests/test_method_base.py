#!/usr/bin/env python
#
# Tests for csdms.dakota.method.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_true, assert_equal
from csdms.dakota.method.base import MethodBase

# Helpers --------------------------------------------------------------


class Concrete(MethodBase):

    """A subclass of MethodBase used for testing."""

    def __init__(self, **kwargs):
        MethodBase.__init__(self, **kwargs)

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = Concrete(method='centered_parameter_study')


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@raises(TypeError)
def test_instantiate():
    """Test whether MethodBase fails to instantiate."""
    d = MethodBase()


def test_get_method():
    """Test getting the method property."""
    assert_true(type(c.method) is str)


def test_set_method():
    """Test setting the method property."""
    m = 'sampling'
    c.method = m
    assert_equal(c.method, m)


@raises(TypeError)
def test_method_fails_if_not_str():
    """Test that setting method to a non-str fails."""
    value = 42
    c.method = value


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 2)
