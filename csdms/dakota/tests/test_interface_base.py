"""Tests for the csdms.dakota.interface.base module."""

import os
from nose.tools import raises, assert_true, assert_false, assert_equal
from csdms.dakota.interface.base import InterfaceBase


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
    b = InterfaceBase()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_asynchronous():
    """Test getting default asynchronous property."""
    value = c.asynchronous
    assert_false(value)


def test_set_asynchronous():
    """Test setting asynchronous property."""
    c.asynchronous = True
    value = c.asynchronous
    assert_true(value)


def test_evaluation_concurrency():
    """Test getting default evaluation_concurrency property."""
    value = c.evaluation_concurrency
    assert_equal(value, default_evaluation_concurrency)


def test_set_evaluation_concurrency():
    """Test setting evaluation_concurrency property."""
    c.evaluation_concurrency = 45
    value = c.evaluation_concurrency
    assert_equal(value, 45)


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
