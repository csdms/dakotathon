"""Tests for the dakotathon.interface.fork module."""

import os
from nose.tools import assert_true, assert_false, assert_equal
from dakotathon.interface.fork import Fork
from .test_interface_base import default_str_lines


run_dir = os.getcwd()
config_file = os.path.join(run_dir, "dakota.yaml")


def setup_module():
    """Fixture called before any tests are performed."""
    print("\n*** " + __name__)
    global f
    f = Fork()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether Fork instantiates."""
    x = Fork()


def test_str_special():
    """Test type of __str__ method results."""
    s = str(f)
    assert_true(type(s) is str)


def test_interface_attribute():
    """Test value of the interface attribute."""
    assert_equal(f.interface, "fork")


# def test_analysis_driver_attribute():
#     """Test value of the analysis_driver attribute."""
#     assert_equal(f.analysis_driver, 'dakota_run_plugin')


def test_config_file_path():
    """Test value of the _configuration_file attribute."""
    assert_equal(f._configuration_file, config_file)


def test_file_attributes():
    """Test value of parameters_file and results_file attributes."""
    assert_equal(f.parameters_file, "params.in")
    assert_equal(f.results_file, "results.out")


def test_str_length():
    """Test the default length of __str__."""
    x = Fork()
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, default_str_lines + 9)
