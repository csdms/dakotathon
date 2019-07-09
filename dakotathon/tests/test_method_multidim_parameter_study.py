#!/usr/bin/env python
#
# Tests for the dakotathon.method.multidim_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_is_instance, assert_true, assert_equal
from dakotathon.method.multidim_parameter_study import MultidimParameterStudy

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print("\n*** " + __name__)
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


def test_method_attr():
    """Test the value of the method attribute."""
    assert_equal(m.method, "multidim_parameter_study")


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


def test_str_special():
    """Test type of __str__ method results."""
    s = str(m)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    m1 = MultidimParameterStudy()
    s = str(m1)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 4)
