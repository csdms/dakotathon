#!/usr/bin/env python
#
# Tests for dakota.methods.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_true, assert_equal
from csdms.dakota.methods.base import MethodsBase

# Helpers --------------------------------------------------------------


class Concrete(MethodsBase):

    """A subclass of MethodsBase used for testing."""

    def __init__(self):
        MethodsBase.__init__(self)

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = Concrete()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@raises(TypeError)
def test_instantiate():
    """Test whether MethodsBase fails to instantiate."""
    d = MethodsBase()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 2)
