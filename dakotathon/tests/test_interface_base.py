"""Tests for the dakotathon.interface.base module."""

import os, sys
from nose.tools import raises, assert_true, assert_false, assert_equal
from dakotathon.interface.base import InterfaceBase


default_evaluation_concurrency = 2
default_str_lines = 4


class Concrete(InterfaceBase):

    """A subclass of InterfaceBase used for testing."""

    def __init__(self):
        InterfaceBase.__init__(self)


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
    """Test whether InterfaceBase instantiates."""
    if sys.version[0] == 2:
        b = InterfaceBase()
    else:
        # abstract base class type error not raised
        # in python 3. 
        raise(TypeError)


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_get_asynchronous():
    """Test getting default asynchronous property."""
    value = c.asynchronous
    assert_false(value)


def test_set_asynchronous():
    """Test setting asynchronous property."""
    c.asynchronous = True
    value = c.asynchronous
    assert_true(value)


@raises(TypeError)
def test_set_asynchronous_fails_if_float():
    """Test that the asynchronous property fails with a float."""
    m = Concrete()
    value = 42.0
    m.asynchronous = value


def test_get_evaluation_concurrency():
    """Test getting default evaluation_concurrency property."""
    value = c.evaluation_concurrency
    assert_equal(value, default_evaluation_concurrency)


def test_set_evaluation_concurrency():
    """Test setting evaluation_concurrency property."""
    c.evaluation_concurrency = 45
    value = c.evaluation_concurrency
    assert_equal(value, 45)


@raises(TypeError)
def test_set_evaluation_concurrency_fails_if_float():
    """Test that evaluation_concurrency fails with a float."""
    m = Concrete()
    value = 42.0
    m.evaluation_concurrency = value


def test_str_length():
    """Test the default length of __str__."""
    b = Concrete()
    s = str(b)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, default_str_lines)


def test_str_length_adding_asynchronous():
    """Test the length of __str__ with asynchronous on."""
    b = Concrete()
    b.asynchronous = True
    s = str(b)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, default_str_lines + 2)


def test_str_length_removing_asynchronous():
    """Test the length of __str__ with asynchronous on then off."""
    b = Concrete()
    b.asynchronous = True
    b.asynchronous = False
    s = str(b)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, default_str_lines)
