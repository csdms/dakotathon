"""Tests for the dakotathon.environment.base module."""

from nose.tools import raises, assert_true, assert_equal
from dakotathon.environment.base import EnvironmentBase


class Concrete(EnvironmentBase):

    """A subclass of EnvironmentBase used for testing."""

    def __init__(self):
        EnvironmentBase.__init__(self)


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = Concrete()


def teardown_module():
    """Called after all tests have completed."""
    pass


@raises(TypeError)
def test_instantiate():
    """Test whether EnvironmentBase fails to instantiate."""
    d = EnvironmentBase()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 1)
