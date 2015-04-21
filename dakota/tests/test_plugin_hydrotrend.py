#!/usr/bin/env python
#
# Tests for the dakota.plugin.hydrotrend module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import filecmp
import tempfile
import numpy as np
from numpy.testing import assert_almost_equal
from nose.tools import raises, with_setup, assert_is_none, assert_true
from dakota.plugins.hydrotrend import HydroTrend
from dakota.utils import get_configuration
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

config_file = os.path.join(data_dir, 'config.yaml')
params_file = os.path.join(data_dir, 'params.in')
known_results_file = os.path.join(data_dir, 'results.out')
results_file = 'results.out'

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global config
    config = get_configuration(params_file)


def setup():
    """Called at start of any test using it @with_setup()"""
    global h
    h = HydroTrend()


def teardown():
    """Called at end of any test using it @with_setup()"""
    pass


def teardown_module():
    """Called after all tests have completed."""
    if os.path.exists(results_file):
        os.remove(results_file)

# Tests ----------------------------------------------------------------


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
    assert_is_none(r)


@with_setup(setup, teardown)
def test_write():
    """Test the write method output versus a known results file."""
    h.output_values = [1.0, 2.0]
    labels = h.write(params_file, results_file)
    assert_true(filecmp.cmp(known_results_file, results_file))
