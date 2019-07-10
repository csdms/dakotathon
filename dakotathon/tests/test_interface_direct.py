"""Tests for the dakotathon.interface.direct module."""

import os
from nose.tools import assert_true, assert_false, assert_equal
from dakotathon.interface.direct import Direct
from .test_interface_base import default_str_lines


def setup_module():
    """Fixture called before any tests are performed."""
    print("\n*** " + __name__)
    global d
    d = Direct()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether Direct instantiates."""
    x = Direct()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(d)
    assert_true(type(s) is str)


def test_interface_attribute():
    """Test value of the interface attribute."""
    assert_equal(d.interface, "direct")


def test_str_length():
    """Test the default length of __str__."""
    b = Direct()
    s = str(b)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, default_str_lines + 1)
