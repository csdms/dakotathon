"""Tests for the csdms.dakota.environment.environment module."""

import os
from nose.tools import assert_true, assert_false, assert_equal
from csdms.dakota.environment.environment import Environment


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global e
    e = Environment()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether Environment instantiates."""
    x = Environment()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(e)
    assert_true(type(s) is str)


def test_data_file_attribute():
    """Test value of the data_file attribute."""
    assert_equal(e.data_file, 'dakota.dat')


def test_str_length():
    """Test the default length of __str__."""
    x = Environment()
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 4)
