#!/usr/bin/env python
#
# Tests for the csdms.dakota.core module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import filecmp
from subprocess import CalledProcessError
from nose.tools import (raises, assert_is_instance, assert_true,
                        assert_is_none, assert_equal)
from csdms.dakota.core import Dakota
from csdms.dakota.utils import is_dakota_installed
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

input_file, \
    output_file, \
    data_file, \
    restart_file = ['dakota.' + ext for ext in ('in', 'out', 'dat', 'rst')]
alt_input_file = 'alt.in'
known_file = os.path.join(data_dir, 'default_vps_dakota.in')
known_config_file = os.path.join(data_dir, 'default_vps_config.yaml')
default_config_file = os.path.join(os.getcwd(), 'config.yaml')
tmp_files = [input_file, alt_input_file, output_file, data_file,
             restart_file, 'config.yaml']

# Fixtures -------------------------------------------------------------


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global d
    d = Dakota()


def teardown_module():
    """Fixture called after all tests have completed."""
    for f in tmp_files:
        if os.path.exists(f):
            os.remove(f)

# Tests ----------------------------------------------------------------


def test_init_no_parameters():
    """Test constructor with no parameters."""
    k = Dakota()
    assert_is_instance(k, Dakota)


def test_init_method_parameter():
    """Test constructor with method parameter."""
    k = Dakota(method='vector_parameter_study')
    assert_is_instance(k, Dakota)


@raises(ImportError)
def test_init_method_parameter_unknown_module():
    """Test constructor with method parameter fails with unknown module."""
    k = Dakota(method='__foo$')


def test_init_from_file_like1():
    """Test creating an instance from a config file."""
    k = Dakota.from_file_like(known_config_file)
    assert_is_instance(k, Dakota)


def test_init_from_file_like2():
    """Test creating an instance from an open config file object."""
    with open(known_config_file, 'r') as fp:
        k = Dakota.from_file_like(fp)
    assert_is_instance(k, Dakota)


def test_get_run_directory():
    """Test getting the run_directory property."""
    assert_equal(d.run_directory, os.getcwd())


def test_set_run_directory():
    """Test setting the run_directory property."""
    k = Dakota()
    run_dir = '/foo/bar'
    k.run_directory = run_dir
    assert_equal(k.run_directory, run_dir)


def test_get_configuration_file():
    """Test getting the configuration_file property."""
    assert_equal(d.configuration_file, default_config_file)


def test_set_configuration_file():
    """Test setting the configuration_file property."""
    k = Dakota()
    k.configuration_file = known_config_file
    assert_equal(k.configuration_file, known_config_file)


def test_get_template_file():
    """Test getting the template_file property."""
    assert_is_none(d.template_file)


def test_set_template_file():
    """Test setting the template_file property."""
    k = Dakota()
    template_file = 'foo.tmpl'
    k.template_file = template_file
    assert_equal(os.path.basename(k.template_file), template_file)


def test_get_auxiliary_files():
    """Test getting the auxiliary_files property."""
    assert_equal(d.auxiliary_files, tuple())


def test_set_auxiliary_files():
    """Test setting the auxiliary_files property."""
    k = Dakota()
    for auxiliary_file in ['foo.in', ['foo.in'], ('foo.in',)]:
        k.auxiliary_files = auxiliary_file
        if type(auxiliary_file) is not str:
            auxiliary_file = auxiliary_file[0]
        pathified_auxiliary_file = os.path.abspath(auxiliary_file)
        assert_equal(k.auxiliary_files, (pathified_auxiliary_file,))


@raises(TypeError)
def test_set_auxiliary_files_fails_if_scalar():
    """Test that auxiliary_files fails with a non-string scalar."""
    k = Dakota()
    auxiliary_file = 42
    k.auxiliary_files = auxiliary_file


def test_write_configuration_file():
    """Test write_configuration_file produces config file."""
    k = Dakota(method='vector_parameter_study')
    k.write_configuration_file()
    assert_true(os.path.exists(k.configuration_file))


def test_write_input_file_with_method_default_name():
    """Test write_input_file works when instanced with method."""
    k = Dakota(method='vector_parameter_study')
    k.write_input_file()
    assert_true(os.path.exists(k.input_file))


def test_write_input_file_with_method_new_name():
    """Test write_input_file works when instanced with method and new name."""
    k = Dakota(method='vector_parameter_study')
    k.write_input_file(input_file=alt_input_file)
    assert_true(os.path.exists(k.input_file))


def test_input_file_contents():
    """Test write_input_file results versus a known input file."""
    k = Dakota(method='vector_parameter_study')
    k.write_input_file()
    assert_true(filecmp.cmp(known_file, input_file))


def test_setup():
    k = Dakota(method='vector_parameter_study')
    k.write_configuration_file()
    k.write_input_file()
    assert_true(os.path.exists(k.configuration_file))
    assert_true(filecmp.cmp(known_file, input_file))


def test_default_run_with_input_file():
    """Test default object run method with input file."""
    if is_dakota_installed():
        k = Dakota()
        k.write_input_file()
        k.run()
        assert_true(os.path.exists(k.output_file))
        assert_true(os.path.exists(k.environment.data_file))


def test_default_run_without_input_file():
    """Test default object run method fails with no input file."""
    if is_dakota_installed():
        if os.path.exists(input_file):
            os.remove(input_file)
        try:
            k = Dakota()
            k.run()
        except CalledProcessError:
            pass
