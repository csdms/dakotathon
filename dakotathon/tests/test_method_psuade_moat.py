#!/usr/bin/env python
#
# Tests for the dakotathon.method.psuade_moat module.
#
# Call with:
#   $ nosetests -sv
#
# Katherine Barnhart (barnhark@colorado.edu)
# after original tests created by
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_is_instance, assert_true, assert_equal
from dakotathon.method.psuade_moat import PsuadeMoat

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global p
    p = PsuadeMoat(seed=395, samples=5)


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------
@raises(TypeError)
def test_init_fails_with_no_parameters():
    """Test that init fails if no parameters are specified."""
    PsuadeMoat()


def test_init_minimum_parameter():
    """Test creating an instance with the minimum number of parameters."""
    p1 = PsuadeMoat(seed=395, samples=5)
    assert_is_instance(p1, PsuadeMoat)


def test_method_attr():
    """Test the value of the method attribute."""
    assert_equal(p.method, 'psuade_moat')

# partition attribute --------------------------------------------------
def test_get_partitions():
    """Test getting the partitions property."""
    assert_true(type(p.partitions) is int)


def test_set_partions():
    """Test setting the partitions property."""
    partitions = 7
    p.partitions = partitions
    assert_equal(p.partitions, partitions)


@raises(TypeError)
def test_set_partition_fails_if_tuple():
    """Test that the partitions property fails with tuple."""
    partitions = (3, 4)
    p.partitions = partitions


# seed attribute --------------------------------------------------
def test_get_seed():
    """Test getting the seed property."""
    assert_true(type(p.seed) is int)


def test_set_seed():
    """Test setting the partitions property."""
    seed = 7
    p.seed = seed
    assert_equal(p.seed, seed)


@raises(TypeError)
def test_set_seed_fails_if_tuple():
    """Test that the seed property fails with tuple."""
    seed = (3, 4)
    p.seed = seed


# samples attribute --------------------------------------------------
def test_get_samples():
    """Test getting the samples property."""
    assert_true(type(p.samples) is int)


def test_set_samples():
    """Test setting the samples property."""
    samples = 7
    p.samples = samples
    assert_equal(p.samples, samples)


@raises(TypeError)
def test_set_samples_fails_if_tuple():
    """Test that the samples property fails with tuple."""
    samples = (3, 4)
    p.samples = samples

# model_pointer attribute --------------------------------------------------
def test_get_model_pointer():
    """Test getting the model_pointer property."""
    assert_true(type(p.model_pointer) is type(None))
    
    p1 = PsuadeMoat(seed=395, samples=5, model_pointer='mymodel')
    assert_true(type(p1.model_pointer) is str)


def test_set_model_pointer():
    """Test setting the model_pointer property."""
    model_pointer = 'my_model'
    p.model_pointer = model_pointer
    assert_equal(p.model_pointer, model_pointer)


@raises(TypeError)
def test_set_model_pointer_fails_if_tuple():
    """Test that the model_pointer property fails with tuple."""
    model_pointer = (3, 4)
    p.model_pointer = model_pointer

def test_str_special():
    """Test type of __str__ method results."""
    s = str(p)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    p1 = PsuadeMoat(seed=395, samples=5)
    s = str(p1)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 6)


def test_model_pointer_str_length():
    """Test the length of __str__ with a model_pointer."""
    p1 = PsuadeMoat(seed=395, samples=5, model_pointer='mymodel')
    s = str(p1)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 7)