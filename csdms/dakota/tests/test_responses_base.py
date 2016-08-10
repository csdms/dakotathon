"""Tests for the csdms.dakota.responses.base module."""

import os
from nose.tools import raises, assert_true, assert_false, assert_equal
from csdms.dakota.responses.base import ResponsesBase


descriptors = ['a', 'b']


class Concrete(ResponsesBase):

    """A subclass of ResponsesBase used for testing."""

    def __init__(self):
        ResponsesBase.__init__(self)


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
    """Test whether ResponsesBase instantiates."""
    r = ResponsesBase()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_responses():
    """Test the default responses attribute."""
    value = c.responses
    assert_equal(value, 'response_functions')


def test_get_response_descriptors():
    """Test getting the response_descriptors property."""
    assert_equal(c.response_descriptors, tuple())


def test_set_response_descriptors():
    """Test setting the response_descriptors property."""
    r = Concrete()
    for desc in [['Qs_median'], ('Qs_median',)]:
        r.response_descriptors = desc
        assert_equal(r.response_descriptors, desc)


@raises(TypeError)
def test_set_response_descriptors_fails_with_nonstring_scalar():
    """Test that response_descriptors fails with a non-string scalar."""
    r = Concrete()
    desc = 42
    r.response_descriptors = desc


def test_set_response_descriptors_string_to_tuple():
    """Test that a string is converted to a tuple."""
    r = Concrete()
    desc = 'x1'
    r.response_descriptors = desc
    assert_true(type(r.response_descriptors) is tuple)


def test_gradients():
    """Test getting the default gradients property."""
    value = c.gradients
    assert_equal(value, 'no_gradients')


def test_hessians():
    """Test getting the default hessians property."""
    value = c.hessians
    assert_equal(value, 'no_hessians')


def test_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 1)
