#!/usr/bin/env python
#
# Tests for the dakota.centered_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import raises, assert_is_instance, assert_true, assert_equal
from csdms.dakota.methods.centered_parameter_study import CenteredParameterStudy
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

config_file = os.path.join(data_dir, 'default_cps_config.yaml')

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = CenteredParameterStudy()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


def test_init_no_params():
    """Test creating an instance with no parameters."""
    c1 = CenteredParameterStudy()
    assert_is_instance(c1, CenteredParameterStudy)


def test_init_from_file_like1():
    """Test creating an instance from a config file."""
    c1 = CenteredParameterStudy.from_file_like(config_file)
    assert_is_instance(c1, CenteredParameterStudy)


def test_init_from_file_like2():
    """Test creating an instance from an open config file object."""
    with open(config_file, 'r') as fp:
        c1 = CenteredParameterStudy.from_file_like(fp)
    assert_is_instance(c1, CenteredParameterStudy)


def test_get_initial_point():
    """Test getting the initial_point property."""
    assert_true(type(c.initial_point) is tuple)


def test_set_initial_point():
    """Test setting the initial_point property."""
    point = (42, 3.14)
    c.initial_point = point
    assert_equal(c.initial_point, point)


@raises(TypeError)
def test_set_initial_point_fails_if_scalar():
    """Test that the initial_point property fails with scalar."""
    point = 42
    c.initial_point = point


def test_get_steps_per_variable():
    """Test getting the steps_per_variable property."""
    assert_true(type(c.steps_per_variable) is tuple)


def test_set_steps_per_variable():
    """Test setting the steps_per_variable property."""
    steps = (2, 3)
    c.steps_per_variable = steps
    assert_equal(c.steps_per_variable, steps)


@raises(TypeError)
def test_set_steps_per_variable_fails_if_scalar():
    """Test that the steps_per_variable property fails with scalar."""
    steps = 2
    c.steps_per_variable = steps


def test_get_step_vector():
    """Test getting the step_vector property."""
    assert_true(type(c.step_vector) is tuple)


def test_set_step_vector():
    """Test setting the step_vector property."""
    steps = (2.0, 3.0)
    c.step_vector = steps
    assert_equal(c.step_vector, steps)


@raises(TypeError)
def test_set_step_vector_fails_if_scalar():
    """Test that the step_vector property fails with scalar."""
    steps = 2.0
    c.step_vector = steps


def test_method_block():
    """Test type of method_block method results."""
    s = c.method_block()
    assert_true(type(s) is str)


def test_variables_block():
    """Test type of variables_block method results."""
    s = c.variables_block()
    assert_true(type(s) is str)
