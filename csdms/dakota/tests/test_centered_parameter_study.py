#!/usr/bin/env python
#
# Tests for the csdms.dakota.methods.centered_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_is_instance, assert_true, assert_equal
from csdms.dakota.methods.centered_parameter_study import CenteredParameterStudy

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


def test_method_attr():
    """Test the value of the method attribute."""
    assert_equal(c.method, 'centered_parameter_study')


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


def test_str_special():
    """Test type of __str__ method results."""
    s = str(c)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    c1 = CenteredParameterStudy()
    s = str(c1)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)
