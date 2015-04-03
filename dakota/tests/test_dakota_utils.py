#!/usr/bin/env python
#
# Tests for dakota.dakota_utils module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import *
from dakota.dakota_utils import *
from . import start_dir, data_dir

# Global variables
parameters_file = os.path.join(data_dir, 'vector_parameter_study_params.in')
response_labels = ['Qs_median']
model = 'hydrotrend'
output_file = 'HYDROASCII.QS'
response_statistic = 'median'

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** dakota_utils tests')

def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------

def test_is_dakota_installed():
    """Test whether Dakota is installed."""
    assert_true(is_dakota_installed())

def test_get_response_descriptors():
    """Test the get_response_descriptors function."""
    assert_equal(response_labels, get_response_descriptors(parameters_file))

def test_get_response_descriptors_unknown_file():
    """Test get_response_descriptors when parameters file not found."""
    assert_is_none(get_response_descriptors('foo.in'))

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
