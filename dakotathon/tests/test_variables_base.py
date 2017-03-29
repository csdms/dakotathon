"""Tests for the dakotathon.variables.base module."""

import os, sys
from nose.tools import raises, assert_true, assert_false, assert_equal
from dakotathon.variables.base import VariablesBase


class Concrete(VariablesBase):

    """A subclass of VariablesBase used for testing."""

    def __init__(self):
        VariablesBase.__init__(self)


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = Concrete()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


@raises(TypeError)
def test_instantiate():
    """Test whether VariablesBase instantiates."""
    if sys.version[0] == 2:
         b = VariablesBase()
    else:
        # abstract base class type error not raised
        # in python 3.
        raise(TypeError)


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_variables():
    """Test getting the default variables property."""
    assert_equal(c.variables, 'continuous_design')


def test_get_descriptors():
    """Test getting the descriptors property."""
    assert_equal(c.descriptors, tuple())


def test_set_descriptors():
    """Test setting the descriptors property."""
    for desc in [['x1'], ('x1',)]:
        c.descriptors = desc
        assert_equal(c.descriptors, desc)


@raises(TypeError)
def test_set_descriptors_fails_if_scalar():
    """Test that descriptors fails with a non-string scalar."""
    desc = 42
    c.descriptors = desc


def test_set_descriptors_string_to_tuple():
    """Test that a string is converted to a tuple."""
    desc = 'x1'
    c.descriptors = desc
    assert_true(type(c.descriptors) is tuple)


def test_str_length():
    """Test the default length of __str__."""
    b = Concrete()
    s = str(b)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 3)
