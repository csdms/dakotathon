"""Tests for the csdms.dakota.responses.response_functions module."""

import os
from nose.tools import raises, assert_true, assert_false, assert_equal
from csdms.dakota.responses.response_functions import ResponseFunctions


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
    for files in [['HYDROASCII.QS'], ('HYDROASCII.QS',)]:
        r.response_files = files
        assert_equal(r.response_files, files)


@raises(TypeError)
def test_set_response_files_fails_if_scalar():
    """Test that the response_files property fails with scalar string."""
    files = 'HYDROASCII.QS'
    r.response_files = files


def test_get_response_statistics():
    """Test getting the default response_statistics property."""
    assert_equal(r.response_statistics, ('mean',))


def test_set_response_statistics():
    """Test setting the response_statistics property."""
    for stats in [['median'], ('median',)]:
        r.response_statistics = stats
        assert_equal(r.response_statistics, stats)


@raises(TypeError)
def test_set_response_statistics_fails_if_scalar():
    """Test that the response_statistics property fails with scalar string."""
    stats = 'median'
    r.response_statistics = stats


def test_str_length():
    """Test the default length of __str__."""
    s = str(r)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)
