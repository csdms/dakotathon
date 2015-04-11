#!/usr/bin/env python
#
# Tests for the dakota.vector_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import *
from dakota.methods.vector_parameter_study import VectorParameterStudy
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

config_file = os.path.join(data_dir, 'hydrotrend_config.yaml')

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

def test_method_block():
    """Test type of method_block method results."""
    s = v.method_block()
    assert_true(type(s) is str)

def test_variables_block():
    """Test type of variables_block method results."""
    s = v.variables_block()
    assert_true(type(s) is str)
