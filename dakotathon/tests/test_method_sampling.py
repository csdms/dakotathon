#!/usr/bin/env python
#
# Tests for the csdms.dakota.method.sampling module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import (raises, assert_is_instance, assert_true,
                        assert_equal, assert_is_none)
from csdms.dakota.method.sampling import Sampling

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global x
    x = Sampling()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


def test_init_no_params():
    """Test creating an instance with no parameters."""
    x1 = Sampling()
    assert_is_instance(x1, Sampling)


def test_method_attr():
    """Test the value of the method attribute."""
    assert_equal(x.method, 'sampling')


def test_str_special():
    """Test type of __str__ method results."""
    s = str(x)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)
