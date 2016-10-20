"""Tests for dakotathon.method.base.UncertaintyQuantificationBase."""

from nose.tools import raises, assert_true, assert_equal, assert_is_none
from dakotathon.method.base import (UncertaintyQuantificationBase,
                                      _print_levels)


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


def test_get_probability_levels():
    """Test getting the probability_levels property."""
    assert_true(type(c.probability_levels) is tuple)


def test_set_probability_levels():
    """Test setting the probability_levels property."""
    m = Concrete()
    for items in [[0,1], (0,1)]:
        m.probability_levels = items
        assert_equal(m.probability_levels, items)


@raises(TypeError)
def test_set_probability_levels_fails_if_scalar():
    """Test that the probability_levels property fails with scalar."""
    m = Concrete()
    pt = 42
    m.probability_levels = pt


def test_get_response_levels():
    """Test getting the response_levels property."""
    assert_true(type(c.response_levels) is tuple)


def test_set_response_levels():
    """Test setting the response_levels property."""
    m = Concrete()
    for items in [[0,1], (0,1)]:
        m.response_levels = items
        assert_equal(m.response_levels, items)


@raises(TypeError)
def test_set_response_levels_fails_if_scalar():
    """Test that the response_levels property fails with scalar."""
    m = Concrete()
    pt = 42
    m.response_levels = pt


def test_get_samples():
    """Test getting the samples property."""
    assert_true(type(c.samples) is int)


def test_set_samples():
    """Test setting the samples property."""
    m = Concrete()
    samples = 42
    m.samples = samples
    assert_equal(m.samples, samples)


@raises(TypeError)
def test_set_samples_fails_if_float():
    """Test that the samples property fails with a float."""
    m = Concrete()
    samples = 42.0
    m.samples = samples


def test_get_sample_type():
    """Test getting the sample_type property."""
    assert_true(c.sample_type == 'random' or c.sample_type == 'lhs')


def test_set_sample_type():
    """Test setting the sample_type property."""
    m = Concrete()
    sample_type = 'lhs'
    m.sample_type = sample_type
    assert_equal(m.sample_type, sample_type)


@raises(TypeError)
def test_set_sample_type_fails_if_not_lhs_or_random():
    """Test that the sample_type property fails with unknown type."""
    m = Concrete()
    sample_type = 'mcmc'
    m.sample_type = sample_type


def test_get_seed1():
    """Test getting the seed property."""
    assert_is_none(c.seed)


def test_get_seed2():
    """Test getting the seed property."""
    m = Concrete(seed=42)
    assert_true(type(m.seed) is int)


def test_set_seed():
    """Test setting the seed property."""
    m = Concrete()
    seed = 42
    m.seed = seed
    assert_equal(m.seed, seed)


@raises(TypeError)
def test_set_seed_fails_if_float():
    """Test that the seed property fails with a float."""
    m = Concrete()
    seed = 42.0
    m.seed = seed


def test_get_variance_based_decomp():
    """Test getting the variance_based_decomp property."""
    assert_true(type(c.variance_based_decomp) is bool)


def test_set_variance_based_decomp():
    """Test setting the variance_based_decomp property."""
    m = Concrete()
    variance_based_decomp = True
    m.variance_based_decomp = variance_based_decomp
    assert_equal(m.variance_based_decomp, variance_based_decomp)


@raises(TypeError)
def test_set_variance_based_decomp_fails_if_float():
    """Test that the variance_based_decomp property fails with a float."""
    m = Concrete()
    variance_based_decomp = 42.0
    m.variance_based_decomp = variance_based_decomp


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_default_str_length():
    """Test the default length of __str__."""
    s = str(c)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 6)


def test_str_length_with_zero_seed_value():
    """Test the length of __str__ with seed = 0."""
    x = Concrete(seed=0)
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)


def test_str_length_with_nonzero_seed_value():
    """Test the length of __str__ with seed != 0."""
    x = Concrete(seed=42)
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 6)


def test_str_length_with_options():
    """Test the length of __str__ with optional props set."""
    x = Concrete(seed=42,
                 probability_levels=range(3),
                 response_levels=range(3),
                 variance_based_decomp=True)
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 8)


def test_print_levels1():
    """Test _print_levels with list and tuple."""
    for item in [[0,1], (0,1)]:
        s = _print_levels(item)
        assert_true(type(s) is str)


def test_print_levels2():
    """Test _print_levels with list of tuples."""
    items = [(1,2,3), (4,5,6)]
    s = _print_levels(items)
    assert_true(type(s) is str)
