#!/usr/bin/env python
#
# Tests for dakota.utils module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import *
from dakota.utils import *
from . import start_dir, data_dir

# Global variables
parameters_file = os.path.join(data_dir, 'vector_parameter_study_params.in')
response_labels = ['Qs_median', 'Q_mean']
config_file = os.path.join(data_dir, 'config.yaml')
component = 'hydrotrend'

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)

def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------

def test_is_dakota_installed():
    """Test whether Dakota is installed."""
    r = is_dakota_installed()
    if os.environ.has_key('TRAVIS'):
        assert_false(r)

def test_get_response_descriptors():
    """Test the get_response_descriptors function."""
    assert_equal(response_labels, get_response_descriptors(parameters_file))

def test_get_response_descriptors_unknown_file():
    """Test get_response_descriptors when parameters file not found."""
    assert_is_none(get_response_descriptors('foo.in'))

def test_get_configuration_filename():
    """Test the get_configuration_filename function."""
    config_filename = get_configuration_filename(parameters_file)
    assert_equal(os.path.basename(config_file), config_filename)

def test_get_configuration_filename_unknown_file():
    """Test get_configuration_filename when parameters file not found."""
    assert_is_none(get_configuration_filename('foo.in'))

def test_get_configuration():
    """Test the get_configuration function."""
    config = get_configuration(config_file)
    assert_equal(component, config.keys()[0])

def test_get_configuration_unknown_file():
    """Test get_configuration when config file not found."""
    assert_is_none(get_configuration('foo.yaml'))

