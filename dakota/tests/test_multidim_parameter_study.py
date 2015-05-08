#!/usr/bin/env python
#
# Tests for the dakota.multidim_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import raises, assert_is_instance, assert_true, assert_equal
from dakota.methods.multidim_parameter_study import MultidimParameterStudy
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

config_file = os.path.join(data_dir, 'default_mps_config.yaml')

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global m
    m = MultidimParameterStudy()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


def test_init_no_params():
    """Test creating an instance with no parameters."""
    m1 = MultidimParameterStudy()
    assert_is_instance(m1, MultidimParameterStudy)


def test_init_from_file_like1():
    """Test creating an instance from a config file."""
    m1 = MultidimParameterStudy.from_file_like(config_file)
    assert_is_instance(m1, MultidimParameterStudy)


def test_init_from_file_like2():
    """Test creating an instance from an open config file object."""
    with open(config_file, 'r') as fp:
        m1 = MultidimParameterStudy.from_file_like(fp)
    assert_is_instance(m1, MultidimParameterStudy)


def test_get_lower_bounds():
    """Test getting the lower_bounds property."""
    assert_true(type(m.lower_bounds) is tuple)


def test_set_lower_bounds():
    """Test setting the lower_bounds property."""
    bound = (42, 3.14)
    m.lower_bounds = bound
    assert_equal(m.lower_bounds, bound)


@raises(TypeError)
def test_set_lower_bounds_fails_if_scalar():
    """Test that the lower_bounds property fails with scalar."""
    bound = 42
    m.lower_bounds = bound


def test_get_upper_bounds():
    """Test getting the upper_bounds property."""
    assert_true(type(m.upper_bounds) is tuple)


def test_set_upper_bounds():
    """Test setting the upper_bounds property."""
    bound = (42, 3.14)
    m.upper_bounds = bound
    assert_equal(m.upper_bounds, bound)


@raises(TypeError)
def test_set_upper_bounds_fails_if_scalar():
    """Test that the upper_bounds property fails with scalar."""
    bound = 42
    m.upper_bounds = bound


def test_get_partitions():
    """Test getting the partitions property."""
    assert_true(type(m.partitions) is tuple)


def test_set_partitions():
    """Test setting the partitions property."""
    breaks = (2, 3)
    m.partitions = breaks
    assert_equal(m.partitions, breaks)


@raises(TypeError)
def test_set_partitions_fails_if_scalar():
    """Test that the partitions property fails with scalar."""
    breaks = 2
    m.partitions = breaks


def test_method_block():
    """Test type of method_block method results."""
    s = m.method_block()
    assert_true(type(s) is str)


def test_variables_block():
    """Test type of variables_block method results."""
    s = m.variables_block()
    assert_true(type(s) is str)
