#!/usr/bin/env python
#
# Tests for dakota.methods.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
from nose.tools import raises, assert_true, assert_is_none, assert_equal
from dakota.methods.base import DakotaBase
from . import start_dir, data_dir

# Helpers --------------------------------------------------------------


class Concrete(DakotaBase):

    """A subclass of DakotaBase used for testing."""

    def __init__(self):
        DakotaBase.__init__(self)
        self.variable_descriptors = ['x0', 'x1']

    def method_block(self):
        return DakotaBase.method_block(self)

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = Concrete()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@raises(TypeError)
def test_instantiate():
    """Test whether DakotaBase fails to instantiate."""
    d = DakotaBase()


def test_get_run_directory():
    """Test getting the run_directory property."""
    assert_equal(c.run_directory, os.getcwd())


def test_set_run_directory():
    """Test setting the run_directory property."""
    run_dir = '/foo/bar'
    c.run_directory = run_dir
    assert_equal(c.run_directory, run_dir)


def test_get_input_files():
    """Test getting the input_files property."""
    assert_equal(c.input_files, tuple())


def test_set_input_files():
    """Test setting the input_files property."""
    input_file = ['foo.in']
    c.input_files = input_file
    assert_equal(c.input_files, input_file)


@raises(TypeError)
def test_set_input_files_fails_if_scalar():
    """Test that the input_files property fails with scalar string."""
    input_file = 'foo.in'
    c.input_files = input_file


def test_environment_block():
    """Test type of environment_block method results."""
    s = c.environment_block()
    assert_true(type(s) is str)


def test_method_block():
    """Test type of method_block method results."""
    s = c.method_block()
    assert_true(type(s) is str)


def test_variables_block():
    """Test type of variables_block method results."""
    s = c.variables_block()
    assert_true(type(s) is str)


def test_interface_block():
    """Test type of interface_block method results."""
    s = c.interface_block()
    assert_true(type(s) is str)


def test_responses_block():
    """Test type of responses_block method results."""
    s = c.responses_block()
    assert_true(type(s) is str)
