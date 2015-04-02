#!/usr/bin/env python
#
# Tests for the dakota.vector_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import *
from dakota.vector_parameter_study import VectorParameterStudy, method


# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** VectorParameterStudy tests')
    global v
    v = VectorParameterStudy()

def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------

def test_method_function():
    """Test the method helper function."""
    assert_equal(v.__class__, method().__class__)

def test_method_block():
    """Test type of method_block method results."""
    s = v.method_block()
    assert_true(type(s) is str)

def test_variables_block():
    """Test type of variables_block method results."""
    s = v.variables_block()
    assert_true(type(s) is str)
