"""Tests for the dakotathon.responses.response_functions module."""

import os
from nose.tools import raises, assert_true, assert_false, assert_equal
from dakotathon.responses.response_functions import ResponseFunctions


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global r
    r = ResponseFunctions()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether ResponsesFunctions instantiates."""
    x = ResponseFunctions()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(r)
    assert_true(type(s) is str)


def test_responses():
    """Test the responses attribute."""
    value = r.responses
    assert_equal(value, 'response_functions')


def test_response_descriptors():
    """Test getting the default response_descriptors property."""
    value = r.response_descriptors
    assert_equal(value, ('y1',))


def test_get_response_files():
    """Test getting the response_files property."""
    assert_equal(r.response_files, tuple())


def test_set_response_files():
    """Test setting the response_files property."""
    x = ResponseFunctions()
    for files in [['HYDROASCII.QS'], ('HYDROASCII.QS',)]:
        x.response_files = files
        assert_equal(x.response_files, files)


@raises(TypeError)
def test_set_response_files_fails_with_nonstring_scalar():
    """Test that response_files fails with a non-string scalar."""
    x = ResponseFunctions()
    value = 42
    x.response_files = value


def test_set_response_files_string_to_tuple():
    """Test that a string is converted to a tuple."""
    x = ResponseFunctions()
    value = 'x1'
    x.response_files = value
    assert_true(type(x.response_files) is tuple)


def test_get_response_statistics():
    """Test getting the default response_statistics property."""
    assert_equal(r.response_statistics, ('mean',))


def test_set_response_statistics():
    """Test setting the response_statistics property."""
    x = ResponseFunctions()
    for stats in [['median'], ('median',)]:
        x.response_statistics = stats
        assert_equal(x.response_statistics, stats)


@raises(TypeError)
def test_set_response_statistics_fails_with_nonstring_scalar():
    """Test that response_statistics fails with a non-string scalar."""
    x = ResponseFunctions()
    value = 42
    x.response_statistics = value


def test_set_response_statistics_string_to_tuple():
    """Test that a string is converted to a tuple."""
    x = ResponseFunctions()
    value = 'x1'
    x.response_statistics = value
    assert_true(type(x.response_statistics) is tuple)


def test_str_length():
    """Test the default length of __str__."""
    s = str(r)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)
