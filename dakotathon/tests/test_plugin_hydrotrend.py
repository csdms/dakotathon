#!/usr/bin/env python
#
# Tests for the dakota.plugin.hydrotrend module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import shutil
import filecmp
import tempfile
import numpy as np
from numpy.testing import assert_almost_equal
from nose.tools import raises, with_setup, assert_is, assert_true
from dakotathon.plugins.hydrotrend import HydroTrend, is_installed
from dakotathon.utils import deserialize
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

run_dir = os.getcwd()
config_file = os.path.join(data_dir, 'config.yaml')
params_file = os.path.join(data_dir, 'params.in')
known_results_file = os.path.join(data_dir, 'results.out')
results_file = 'results.out'

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)


def setup():
    """Called at start of any test using it @with_setup()"""
    global h, config
    h = HydroTrend()
    config = deserialize(config_file)


def teardown():
    """Called at end of any test using it @with_setup()"""
    if os.path.exists(results_file):
        os.remove(results_file)
    if os.path.exists(h.input_dir):
        shutil.rmtree(h.input_dir)
    if os.path.exists(h.output_dir):
        shutil.rmtree(h.output_dir)


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@with_setup(setup, teardown)
def test_setup_files():
    """Tests setup_files() against the sample configuration file."""
    r = h.setup_files(config)
    assert_is(h.input_template, config['template_file'])
    assert_is(h.hypsometry_file, config['auxiliary_files'][0])
    assert_is(h.output_files, config['response_files'])
    assert_is(h.output_statistics, config['response_statistics'])


@with_setup(setup, teardown)
def test_setup_directories():
    """Tests setup_directories() against the sample configuration file."""
    config['run_directory'] = run_dir
    r = h.setup_directories(config)
    assert_true(os.path.exists(h.input_dir))
    assert_true(os.path.exists(h.output_dir))


@with_setup(setup, teardown)
def test_call_without_setup():
    """Tests that call() fails without input/output directories."""
    if is_installed():
        r = h.call()
        assert_is(r, None)


@with_setup(setup, teardown)
def test_load():
    """Tests load() with a text file."""
    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        fp.write('h1\nh2\n0\n1\n2\n')
        output_file = fp.name
    r = h.load(output_file)
    assert_almost_equal(r, np.arange(3, dtype=float))
    os.remove(output_file)


@raises(TypeError)
@with_setup(setup, teardown)
def test_load_zero_arguments():
    """Tests load() when no argument is passed."""
    r = h.load()


@with_setup(setup, teardown)
def test_load_does_not_exist():
    """Tests load() when a nonexistent output file is defined."""
    r = h.load('vfnqeubnuen.f')
    assert_is(r, None)


@with_setup(setup, teardown)
def test_write():
    """Test the write method output versus a known results file."""
    h.output_values = [1.0, 2.0]
    h.write(params_file, results_file)
    assert_true(filecmp.cmp(known_results_file, results_file))
