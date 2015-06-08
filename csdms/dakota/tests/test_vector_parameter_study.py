#!/usr/bin/env python
#
# Tests for the dakota.vector_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import raises, assert_is_instance, assert_true, assert_equal
from dakota.methods.vector_parameter_study import VectorParameterStudy
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

config_file = os.path.join(data_dir, 'default_vps_config.yaml')

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global v
    v = VectorParameterStudy()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


def test_init_no_params():
    """Test creating an instance with no parameters."""
    v1 = VectorParameterStudy()
    assert_is_instance(v1, VectorParameterStudy)


def test_init_from_file_like1():
    """Test creating an instance from a config file."""
    v1 = VectorParameterStudy.from_file_like(config_file)
    assert_is_instance(v1, VectorParameterStudy)


def test_init_from_file_like2():
    """Test creating an instance from an open config file object."""
    with open(config_file, 'r') as fp:
        v1 = VectorParameterStudy.from_file_like(fp)
    assert_is_instance(v1, VectorParameterStudy)


def test_get_initial_point():
    """Test getting the initial_point property."""
    assert_true(type(v.initial_point) is tuple)


def test_set_initial_point():
    """Test setting the initial_point property."""
    point = (42,)
    v.initial_point = point
    assert_equal(v.initial_point, point)


@raises(TypeError)
def test_set_initial_point_fails_if_scalar():
    """Test that the initial_point property fails with scalar."""
    point = 42
    v.initial_point = point


def test_get_final_point():
    """Test getting the final_point property."""
    assert_true(type(v.final_point) is tuple)


def test_set_final_point():
    """Test setting the final_point property."""
    point = (42,)
    v.final_point = point
    assert_equal(v.final_point, point)


@raises(TypeError)
def test_set_final_point_fails_if_scalar():
    """Test that the final_point property fails with scalar."""
    point = 42
    v.final_point = point


def test_method_block():
    """Test type of method_block method results."""
    s = v.method_block()
    assert_true(type(s) is str)


def test_variables_block():
    """Test type of variables_block method results."""
    s = v.variables_block()
    assert_true(type(s) is str)
