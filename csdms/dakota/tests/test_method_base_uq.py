"""Tests for csdms.dakota.method.base.UncertaintyQuantificationBase."""

from nose.tools import raises, assert_true, assert_equal
from csdms.dakota.method.base import UncertaintyQuantificationBase


class Concrete(UncertaintyQuantificationBase):

    """A subclass of UncertaintyQuantificationBase used for testing."""

    def __init__(self, **kwargs):
        UncertaintyQuantificationBase.__init__(self, **kwargs)


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
    """Test whether UncertaintyQuantificationBase fails to instantiate."""
    d = UncertaintyQuantificationBase()


def test_get_basis_polynomial_family():
    """Test getting the basis_polynomial_family property."""
    assert_true(type(c.basis_polynomial_family) is str)


def test_set_basis_polynomial_family():
    """Test setting the basis_polynomial_family property."""
    m = 'askey'
    c.basis_polynomial_family = m
    assert_equal(c.basis_polynomial_family, m)


@raises(TypeError)
def test_basis_polynomial_family_fails_if_unknown_type():
    """Test that setting basis_polynomial_family to an unknown type fails."""
    value = 'foobar'
    c.basis_polynomial_family = value


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 3)
