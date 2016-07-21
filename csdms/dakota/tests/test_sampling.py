#!/usr/bin/env python
#
# Tests for the csdms.dakota.methods.sampling module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import (raises, assert_is_instance, assert_true,
                        assert_equal, assert_is_none)
from csdms.dakota.methods.sampling import Sampling

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


def test_get_samples():
    """Test getting the samples property."""
    assert_true(type(x.samples) is int)


def test_set_samples():
    """Test setting the samples property."""
    samples = 42
    x.samples = samples
    assert_equal(x.samples, samples)


@raises(TypeError)
def test_set_samples_fails_if_float():
    """Test that the samples property fails with a float."""
    samples = 42.0
    x.samples = samples


def test_get_sample_type():
    """Test getting the sample_type property."""
    assert_true(x.sample_type == 'random' or x.sample_type == 'lhs')


def test_set_sample_type():
    """Test setting the sample_type property."""
    sample_type = 'lhs'
    x.sample_type = sample_type
    assert_equal(x.sample_type, sample_type)


@raises(TypeError)
def test_set_sample_type_fails_if_not_lhs_or_random():
    """Test that the sample_type property fails with unknown type."""
    sample_type = 'mcmc'
    x.sample_type = sample_type


def test_get_seed():
    """Test getting the seed property."""
    if x.seed is not None:
        assert_true(type(x.seed) is int)
    else:
        assert_is_none(x.seed)


def test_set_seed():
    """Test setting the seed property."""
    seed = 42
    x.seed = seed
    assert_equal(x.seed, seed)


@raises(TypeError)
def test_set_seed_fails_if_float():
    """Test that the seed property fails with a float."""
    seed = 42.0
    x.seed = seed


def test_str_special():
    """Test type of __str__ method results."""
    s = str(x)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    x1 = Sampling()
    s = str(x1)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)
