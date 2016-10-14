#!/usr/bin/env python
#
# Tests for the dakota.run_plugin module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import sys
import shutil
# import filecmp
# import tempfile
# import numpy as np
# from numpy.testing import assert_almost_equal
from nose.tools import raises, with_setup
from dakotathon.run_plugin import run_plugin, main
from dakotathon.dakota import Dakota
from dakotathon.plugins.hydrotrend import is_installed
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

run_dir = os.getcwd()
local_config_file = 'config.yaml'
config_file = os.path.join(data_dir, local_config_file)
local_params_file = 'params.in'
params_file = os.path.join(data_dir, local_params_file)
results_file = 'results.out'

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)


def setup():
    """Called at start of any test using it @with_setup()"""
    global d
    d = Dakota.from_file_like(config_file)


def teardown():
    """Called at end of any test using it @with_setup()"""
    if os.path.exists(results_file):
        os.remove(results_file)
    if os.path.exists(local_config_file):
        os.remove(local_config_file)
    if os.path.exists(local_params_file):
        os.remove(local_params_file)


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


# @with_setup(setup, teardown)
# def test_run_plugin():
#     """Tests run_plugin()."""
#     if is_installed():
#         shutil.copy(params_file, run_dir)
#         shutil.copy(config_file, run_dir)
#         run_plugin(params_file, results_file)


@raises(IOError)
def test_run_plugin_unknown_config_file():
    """Tests run_plugin() fails with unknown config file."""
    run_plugin(params_file, results_file)


@raises(ImportError)
@with_setup(setup, teardown)
def test_run_plugin_unknown_module():
    """Tests run_plugin() fails with unknown module."""
    d.method.component = 'foo'
    d.serialize(local_config_file)
    run_plugin(params_file, results_file)


@raises(NameError)
@with_setup(setup, teardown)
def test_run_plugin_uninstalled_module():
    """Tests run_plugin() fails with module that's not installed."""
    d.serialize(local_config_file)
    os.environ['PATH'] = '.'
    run_plugin(params_file, results_file)


@raises(IndexError)
def test_main_no_args():
    """Tests main() fails without args."""
    sys.argv = []
    main()
