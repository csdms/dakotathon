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
from dakota.dakota import Dakota

# Global variables
start_dir = os.getcwd()
data_dir = os.path.join(start_dir, 'dakota', 'tests', 'data')
input_file = 'dakota.in'
alt_input_file = 'alt.in'
known_file = os.path.join(data_dir, 'dakota.in')

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

def test_run():
    """Test the run method."""
    print(d.method, d.analysis_driver)
    if not os.path.exists(d.input_file):
        d.create_input_file('test.in')
    d.run()
    assert_true(os.path.exists(d.input_file))
    assert_true(os.path.exists(d.output_file))
    assert_true(os.path.exists(d.data_file))
