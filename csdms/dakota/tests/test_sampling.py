#!/usr/bin/env python
#
# Tests for the dakota.methods.sampling module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import (raises, assert_is_instance, assert_true,
                        assert_equal, assert_is_none)
from csdms.dakota.methods.sampling import Sampling
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

config_file = os.path.join(data_dir, 'default_sampling_config.yaml')

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


def test_init_from_file_like1():
    """Test creating an instance from a config file."""
    x1 = Sampling.from_file_like(config_file)
    assert_is_instance(x1, Sampling)


def test_init_from_file_like2():
    """Test creating an instance from an open config file object."""
    with open(config_file, 'r') as fp:
        x1 = Sampling.from_file_like(fp)
    assert_is_instance(x1, Sampling)


def test_get_lower_bounds():
    """Test getting the lower_bounds property."""
    assert_true(type(x.lower_bounds) is tuple)


def test_set_lower_bounds():
    """Test setting the lower_bounds property."""
    bound = (42, 3.14)
    x.lower_bounds = bound
    assert_equal(x.lower_bounds, bound)


@raises(TypeError)
def test_set_lower_bounds_fails_if_scalar():
    """Test that the lower_bounds property fails with scalar."""
    bound = 42
    x.lower_bounds = bound


def test_get_upper_bounds():
    """Test getting the upper_bounds property."""
    assert_true(type(x.upper_bounds) is tuple)


def test_set_upper_bounds():
    """Test setting the upper_bounds property."""
    bound = (42, 3.14)
    x.upper_bounds = bound
    assert_equal(x.upper_bounds, bound)


@raises(TypeError)
def test_set_upper_bounds_fails_if_scalar():
    """Test that the upper_bounds property fails with scalar."""
    bound = 42
    x.upper_bounds = bound


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


def test_method_block():
    """Test type of method_block method results."""
    s = x.method_block()
    assert_true(type(s) is str)


def test_variables_block():
    """Test type of variables_block method results."""
    s = x.variables_block()
    assert_true(type(s) is str)
