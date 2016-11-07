#!/usr/bin/env python
#
# Tests for dakota.utils module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import (raises, assert_equal, assert_false, assert_true,
                        assert_is_none)
from dakotathon.utils import *
from . import start_dir, data_dir

# Global variables -----------------------------------------------------

parameters_file = os.path.join(data_dir, 'params.in')
results_file = 'results.out'
response_labels = ['Qs_median', 'Q_mean']
config_file = os.path.join(data_dir, 'dakota.yaml')
plugin = 'hydrotrend'

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


def test_which():
    """Test the 'which' function."""
    r = which('python')


def test_which_fails_with_nonexistent_program():
    """Test that which fails with a nonexistent program."""
    r = which('vvwuvnfub')
    assert_is_none(r)


def test_which_dakota():
    """Test the 'which_dakota' function."""
    r = which_dakota()
    if 'TRAVIS' in os.environ:
        assert_is_none(r)


def test_add_dyld_library_path():
    """Test the 'add_dyld_library_path' function."""
    r = add_dyld_library_path()
    if 'TRAVIS' in os.environ:
        assert_is_none(r)


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


@raises(IOError)
def test_get_configuration_file_unknown_file():
    """Test get_configuration_file when parameters file not found."""
    get_configuration_file('foo.in')


def test_deserialize():
    """Test the deserialize function."""
    config = deserialize(config_file)
    assert_equal(plugin, config['plugin'])


@raises(IOError)
def test_deserialize_unknown_file():
    """Test deserialize when config file not found."""
    deserialize('foo.yaml')


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


def test_write_results_scalar_input():
    """Test the write_results function works with scalar inputs."""
    values = 1.0
    labels = 'foo'
    r = write_results(results_file, values, labels)


def test_to_iterable_with_scalar():
    """Test that to_iterable returns a tuple with scalar input."""
    value = 'foo'
    r = to_iterable(value)
    assert_true(type(r) is tuple)


def test_to_iterable_with_tuple():
    """Test that to_iterable returns original tuple with tuple input."""
    value = ('foo',)
    r = to_iterable(value)
    assert_true(r is value)


def test_to_iterable_with_list():
    """Test that to_iterable returns original list with list input."""
    value = ['foo']
    r = to_iterable(value)
    assert_true(r is value)


@raises(KeyError)
def test_configure_parameters_fails_without_descriptors():
    """Test that configure_parameters fails without descriptors."""
    params = {}
    r = configure_parameters(params)


def test_configure_parameters_sets_plugin_and_component():
    """Test that configure_parameters sets analysis_driver for component."""
    params = {'descriptors': 'foo', 'response_descriptors': 'bar',
              'response_statistics': 'baz'}
    updated, subs = configure_parameters(params)
    assert_equal(updated['component'], '')
    assert_equal(updated['plugin'], '')


def test_configure_parameters_return_values():
    """Test configure_parameters return values."""
    params = {'descriptors': 'foo', 'response_descriptors': 'bar',
              'response_statistics': 'baz'}
    updated, subs = configure_parameters(params)
    assert_equal(updated['component'], '')
    assert_equal(updated['plugin'], '')


def test_configure_parameters_sets_analysis_driver_component():
    """Test that configure_parameters sets analysis_driver for component."""
    params = {'descriptors': 'foo', 'response_descriptors': 'bar',
              'response_statistics': 'baz'}
    params['component'] = 'model'
    r = configure_parameters(params)
    assert_equal(type(r), tuple)
    assert_equal(type(r[0]), dict)
    assert_equal(type(r[1]), dict)


def test_configure_parameters_sets_analysis_driver_plugin():
    """Test that configure_parameters sets analysis_driver for plugin."""
    params = {'descriptors': 'foo', 'response_descriptors': 'bar',
              'response_statistics': 'baz'}
    params['plugin'] = 'model'
    updated, subs = configure_parameters(params)
    assert_equal(updated['analysis_driver'], 'dakota_run_plugin')
    assert_equal(updated['component'], '')
