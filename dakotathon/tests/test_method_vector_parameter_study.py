#!/usr/bin/env python
#
# Tests for the dakotathon.method.vector_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_is_instance, assert_true, assert_equal
from dakotathon.method.vector_parameter_study import VectorParameterStudy

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print("\n*** " + __name__)
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


def test_method_attr():
    """Test the value of the method attribute."""
    assert_equal(v.method, "vector_parameter_study")


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


def test_get_n_steps():
    """Test getting the n_steps property."""
    assert_true(type(v.n_steps) is int)


def test_set_n_steps():
    """Test setting the n_steps property."""
    n = 42
    v.n_steps = n
    assert_equal(v.n_steps, n)


@raises(TypeError)
def test_n_steps_fails_if_not_int():
    """Test that setting n_steps to a non-int fails."""
    value = 42.0
    v.n_steps = value


def test_str_special():
    """Test type of __str__ method results."""
    s = str(v)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    v1 = VectorParameterStudy()
    s = str(v1)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 5)
