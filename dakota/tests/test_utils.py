#!/usr/bin/env python
#
# Tests for dakota.utils module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import raises, assert_equal, assert_false, assert_is_none
from dakota.utils import *
from . import start_dir, data_dir

# Global variables -----------------------------------------------------

parameters_file = os.path.join(data_dir, 'params.in')
results_file = 'results.out'
response_labels = ['Qs_median', 'Q_mean']
config_file = os.path.join(data_dir, 'config.yaml')
component = 'hydrotrend'

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)


def teardown_module():
    """Called after all tests have completed."""
    if os.path.exists(results_file):
        os.remove(results_file)

# Tests ----------------------------------------------------------------


def test_is_dakota_installed():
    """Test whether Dakota is installed."""
    r = is_dakota_installed()
    if 'TRAVIS' in os.environ:
        assert_false(r)


def test_get_response_descriptors():
    """Test the get_response_descriptors function."""
    assert_equal(response_labels, get_response_descriptors(parameters_file))


def test_get_response_descriptors_unknown_file():
    """Test get_response_descriptors when parameters file not found."""
    assert_is_none(get_response_descriptors('foo.in'))


def test_get_configuration_file():
    """Test the get_configuration_file function."""
    config_file = get_configuration_file(parameters_file)
    assert_equal(os.path.basename(config_file), config_file)


def test_get_configuration_file_unknown_file():
    """Test get_configuration_file when parameters file not found."""
    assert_is_none(get_configuration_file('foo.in'))


def test_get_configuration():
    """Test the get_configuration function."""
    config = get_configuration(config_file)
    assert_equal(component, config['component'])


def test_get_configuration_unknown_file():
    """Test get_configuration when config file not found."""
    assert_is_none(get_configuration('foo.yaml'))


def test_compute_statistic():
    """Test the compute_statistic function."""
    stat = 'mean'
    arr = range(6)
    assert_equal(2.5, compute_statistic(stat, arr))


@raises(AttributeError)
def test_compute_statistic_unknown_statistic():
    """Test the compute_statistic function fails with an unknown statistic."""
    stat = 'foo'
    arr = range(6)
    r = compute_statistic(stat, arr)


@raises(TypeError)
def test_compute_statistic_nonumeric_array():
    """Test the compute_statistic function fails with a nonumeric array."""
    stat = 'mean'
    arr = ['hi', 'there']
    r = compute_statistic(stat, arr)

@raises(TypeError)
def test_write_results_scalar_input():
    """Test the write_results function fails with scalar inputs."""
    values = 1.0
    labels = 'foo'
    r = write_results(results_file, values, labels)
