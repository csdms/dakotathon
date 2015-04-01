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
alt_input_file = 'alt.in'
known_file = os.path.join(data_dir, 'vector_parameter_study.in')

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** VectorParameterStudy tests')
    global v
    v = VectorParameterStudy()

def teardown_module():
    """Called after all tests have completed."""
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(alt_input_file):
        os.remove(alt_input_file)

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
    v.n_responses = len(v.response_descriptors)
    v.response_files = ['HYDROASCII.QS', 'HYDROASCII.Q']
    v.response_statistics = ['median', 'mean']

def teardown():
    """Called at end of any test using it @with_setup()"""
    pass

# Tests ----------------------------------------------------------------

def test_run():
    """Test the run method."""
    print(v.method, v.analysis_driver)
    v.run()

def test_create_default_input_file():
    """Test the create_input_file method with default parameters."""
    v.create_input_file()
    assert_true(os.path.exists(input_file))

def test_create_alt_input_file():
    """Test the create_input_file method with an alternate name."""
    v.create_input_file(alt_input_file)
    assert_true(os.path.exists(alt_input_file))

@with_setup(setup, teardown)
def test_create_input_file():
    """Test the create_input_file method with experiment parameters."""
    v.create_input_file()
    assert_true(os.path.exists(input_file))

@with_setup(setup, teardown)
def test_input_file_contents():
    """Test create_input_file method results versus a known input file."""
    v.create_input_file()
    assert_true(filecmp.cmp(known_file, input_file))
