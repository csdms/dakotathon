#!/usr/bin/env python
#
# Tests for the dakota.vector_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import filecmp
from nose.tools import *
from dakota.vector_parameter_study import VectorParameterStudy

# Global variables
start_dir = os.getcwd()
data_dir = os.path.join(start_dir, 'tests', 'data')
input_file = 'dakota.in'
known_file = os.path.join(data_dir, 'vector_parameter_study.in')

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('*** VectorParameterStudy tests')
    global v
    v = VectorParameterStudy()

def teardown_module():
    """Called after all tests have completed."""
    if os.path.exists(input_file):
        os.remove(input_file)

def setup():
    """Called at start of any test using it @with_setup()"""
    v.model = 'hydrotrend'
    v.input_file = input_file
    v.variable_descriptors = ['T', 'P']
    v.n_variables = len(v.variable_descriptors)
    v.initial_point = [10.0, 1.5]
    v.final_point = [20.0, 2.5]
    v.n_steps = 6
    v.interface = 'fork'
    v.analysis_driver = 'run_model.py'
    v.response_descriptors = ['Qs_median', 'Q_mean']
    v.n_response_functions = len(v.response_descriptors)
    v.response_files = ['HYDROASCII.QS', 'HYDROASCII.Q']
    v.response_statistics = ['median', 'mean']

def teardown():
    """Called at end of any test using it @with_setup()"""
    if os.path.exists(input_file):
        os.remove(input_file)

# Tests ----------------------------------------------------------------

def test_run():
    """Test the run method."""
    v.run()

def test_default_write():
    """Test the write method with default/empty parameters."""
    v.write()
    assert_true(os.path.exists(input_file))

@with_setup(setup, teardown)
def test_write():
    """Test the write method with experiment parameters."""
    v.write()
    assert_true(os.path.exists(input_file))

@with_setup(setup, teardown)
def test_write_contents():
    """Test write method results versus a known input file."""
    v.write()
    assert_true(filecmp.cmp(known_file, input_file))
