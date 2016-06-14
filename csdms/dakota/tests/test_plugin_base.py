# Tests for dakota.plugins.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import filecmp
from nose.tools import raises, assert_is_none, assert_true
from csdms.dakota.plugins.base import (PluginBase, write_dflt_file,
                                       write_dtmpl_file)
from . import start_dir, data_dir

# Helpers --------------------------------------------------------------


class Concrete(PluginBase):

    """A subclass of PluginBase used for testing."""

    def __init__(self):
        PluginBase.__init__(self)

    def setup(self):
        return PluginBase.setup(self, None)

    def call(self):
        return PluginBase.call(self)

    def load(self):
        return PluginBase.load(self, None)

    def calculate(self):
        return PluginBase.calculate(self)

    def write(self):
        return PluginBase.write(self, None, None)

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
    """Test whether PluginBase fails to instantiate."""
    d = PluginBase()


def test_setup():
    """Test type of setup method results."""
    s = c.setup()
    assert_is_none(s)


def test_call():
    """Test type of call method results."""
    s = c.call()
    assert_is_none(s)


def test_load():
    """Test type of load method results."""
    s = c.load()
    assert_is_none(s)


def test_calculate():
    """Test type of calculate method results."""
    s = c.calculate()
    assert_is_none(s)


def test_write():
    """Test type of write method results."""
    s = c.write()
    assert_is_none(s)


def test_write_dflt_file():
    """Test the 'write_dflt_file' function versus a known dflt file."""
    known_dflt_file = os.path.join(data_dir, 'HYDRO.IN.defaults')
    tmpl_file = os.path.join(data_dir, 'hydrotrend.in.tmpl')
    parameters_file = os.path.join(data_dir, 'parameters.yaml')
    dflt_file = write_dflt_file(tmpl_file, parameters_file)
    assert_true(len(known_dflt_file), len(dflt_file))
    os.remove(dflt_file)


def test_write_dtmpl_file():
    """Test the 'write_dtmpl_file' function against a known dtmpl file."""
    known_dtmpl_file = os.path.join(data_dir, 'HYDRO.IN.dtmpl')
    tmpl_file = os.path.join(data_dir, 'hydrotrend.in.tmpl')
    base_input_file = os.path.join(data_dir, 'HYDRO.IN.defaults')
    parameter_names = ['starting_mean_annual_temperature',
                       'total_annual_precipitation']
    dtmpl_file = write_dtmpl_file(tmpl_file,
                                  base_input_file,
                                  parameter_names)
    assert_true(filecmp.cmp(known_dtmpl_file, dtmpl_file))
    os.remove(dtmpl_file)
