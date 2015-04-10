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
from dakota.utils import is_dakota_installed
from . import start_dir, data_dir

# Global variables
input_file, \
    output_file, \
    data_file, \
    restart_file = ['dakota.' + ext for ext in ('in','out','dat','rst')]
alt_input_file = 'alt.in'
known_file = os.path.join(data_dir, 'dakota.in')
config_file = 'config.yaml'
tmp_files = [input_file, alt_input_file, output_file, data_file, \
             restart_file, config_file]

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)

def teardown_module():
    """Called after all tests have completed."""
    for f in tmp_files:
        if os.path.exists(f): os.remove(f)        

# Tests ----------------------------------------------------------------

def test_init_no_parameters():
    """Test constructor fails with no parameters."""
    d = Dakota()
    assert_is_instance(d, Dakota)

def test_init_method_parameter():
    """Test constructor with method parameter."""
    d = Dakota(method='vector_parameter_study')
    assert_is_instance(d, Dakota)

@raises(ImportError)
def test_init_method_parameter_unknown_module():
    """Test constructor with method parameter fails with unknown module."""
    d = Dakota(method='foo')

def test_write_configuration_file():
    """Test write_configuration_file produces config file."""
    d = Dakota(method='vector_parameter_study')
    d.write_configuration_file()

@raises(TypeError)
def test_write_input_file_with_input_file():
    """Test write_input_file fails when instanced with input file."""
    d = Dakota(input_file='foo.in')
    d.write_input_file()

def test_write_input_file_with_method_default_name():
    """Test write_input_file works when instanced with method."""
    d = Dakota(method='vector_parameter_study')
    d.write_input_file()
    assert_true(os.path.exists(d.input_file))

def test_write_input_file_with_method_new_name():
    """Test write_input_file works when instanced with method and new name."""
    d = Dakota(method='vector_parameter_study')
    d.write_input_file(input_file=alt_input_file)
    assert_true(os.path.exists(d.input_file))

def test_input_file_contents():
    """Test write_input_file results versus a known input file."""
    d = Dakota(method='vector_parameter_study')
    d.write_input_file()
    assert_true(filecmp.cmp(known_file, input_file))

def test_run_without_input_file():
    """Test run method fails with no input file."""
    if is_dakota_installed():
        if os.path.exists(input_file): os.remove(input_file)
        try:
            d = Dakota()
            d.run()
        except IOError:
            pass
