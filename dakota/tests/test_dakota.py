#!/usr/bin/env python
#
# Tests for dakota.dakota module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import filecmp
from nose.tools import *
from dakota.dakota import is_dakota_installed, Dakota, get_labels, \
    get_analysis_components

# Global variables
start_dir = os.getcwd()
data_dir = os.path.join(start_dir, 'dakota', 'tests', 'data')
input_file = 'dakota.in'
alt_input_file = 'alt.in'
known_file = os.path.join(data_dir, 'dakota.in')
parameters_file = os.path.join(data_dir, 'vector_parameter_study_params.in')
response_labels = ['Qs_median']
model = 'hydrotrend'
output_file = 'HYDROASCII.QS'
response_statistic = 'median'

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** Dakota tests')
    global d
    d = Dakota()

def teardown_module():
    """Called after all tests have completed."""
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(alt_input_file):
        os.remove(alt_input_file)
    if os.path.exists(d.output_file):
        os.remove(d.output_file)
    if os.path.exists(d.data_file):
        os.remove(d.data_file)
    if os.path.exists('dakota.rst'):
        os.remove('dakota.rst')

# Tests ----------------------------------------------------------------

def test_is_dakota_installed():
    """Test whether Dakota is installed."""
    assert_true(is_dakota_installed)

def test_constructor_alt_input_file():
    """Test calling the constructor with an input file."""
    d1 = Dakota(alt_input_file)
    assert_equal(d1.input_file, alt_input_file)

def test_create_default_input_file():
    """Test the create_input_file method with default parameters."""
    d.create_input_file()
    assert_true(os.path.exists(input_file))

def test_create_alt_input_file():
    """Test the create_input_file method with an alternate name."""
    d.create_input_file(alt_input_file)
    assert_true(os.path.exists(alt_input_file))

def test_input_file_contents():
    """Test create_input_file method results versus a known input file."""
    d.create_input_file()
    assert_true(filecmp.cmp(known_file, input_file))

def test_environment_block():
    """Test type of environment_block method results."""
    s = d.environment_block()
    assert_true(type(s) is str)

def test_method_block():
    """Test type of method_block method results."""
    s = d.method_block()
    assert_true(type(s) is str)

def test_variables_block():
    """Test type of variables_block method results."""
    s = d.variables_block()
    assert_true(type(s) is str)

def test_interface_block():
    """Test type of interface_block method results."""
    s = d.interface_block()
    assert_true(type(s) is str)

def test_responses_block():
    """Test type of responses_block method results."""
    s = d.responses_block()
    assert_true(type(s) is str)

def test_get_labels():
    """Test the get_labels function."""
    assert_equal(response_labels, get_labels(parameters_file))

def test_get_labels_unknown_file():
    """Test get_labels when parameters file not found."""
    assert_is_none(get_labels('foo.in'))

def test_get_analysis_components():
    """Test the get_analysis_components function."""
    ac = get_analysis_components(parameters_file)
    assert_equal(model, ac.pop(0))
    response = ac.pop(0)
    assert_equal(response['file'], output_file)
    assert_equal(response['statistic'], response_statistic)

def test_get_analysis_components_unknown_file():
    """Test get_analysis_components when parameters file not found."""
    assert_is_none(get_analysis_components('foo.in'))

def test_run():
    """Test the run method."""
    print(d.method, d.analysis_driver)
    if not os.path.exists(d.input_file):
        d.create_input_file('test.in')
    d.run()
    assert_true(os.path.exists(d.input_file))
    assert_true(os.path.exists(d.output_file))
    assert_true(os.path.exists(d.data_file))
