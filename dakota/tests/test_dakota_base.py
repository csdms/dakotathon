#!/usr/bin/env python
#
# Tests for dakota.methods.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_true, assert_is_none
from dakota.methods.base import DakotaBase
from . import start_dir, data_dir

# Helpers --------------------------------------------------------------


class Concrete(DakotaBase):

    """A subclass of DakotaBase used for testing."""

    def __init__(self):
        DakotaBase.__init__(self)

    def method_block(self):
        pass

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


def test_environment_block():
    """Test type of environment_block method results."""
    s = c.environment_block()
    assert_true(type(s) is str)


def test_method_block():
    """Test type of method_block method results."""
    s = c.method_block()
    assert_is_none(s)


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
