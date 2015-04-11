#!/usr/bin/env python
#
# Tests for the dakota.plugin.hydrotrend module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import *
from dakota.plugins.hydrotrend import HydroTrend
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global h
    h = HydroTrend()

def setup():
    """Called at start of any test using it @with_setup()"""
    pass

def teardown():
    """Called at end of any test using it @with_setup()"""
    pass

def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------

@raises(TypeError)
def test_load_zero_arguments():
    """Tests load() when no argument is passed."""
    r = h.load()

def test_load_does_not_exist():
    """Tests load() when a nonexistent output file is defined."""
    r = h.load('vfnqeubnuen.f')
    assert_is_none(r)
