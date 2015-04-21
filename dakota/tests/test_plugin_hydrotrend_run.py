#!/usr/bin/env python
#
# Test running the dakota.plugin.hydrotrend module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import shutil
import glob
from nose.tools import with_setup, assert_true
from dakota.core import Dakota
from dakota.plugins.hydrotrend import is_installed as is_hydrotrend_installed
from dakota.utils import is_dakota_installed
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

run_dir = os.getcwd()
config_file = os.path.join(run_dir, 'config.yaml')
existing_config_file = os.path.join(data_dir, 'config.yaml')

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)


def setup():
    """Called at start of any test using it @with_setup()"""
    pass


def teardown():
    """Called at end of any test using it @with_setup()"""
    if is_dakota_installed():
        for dname in glob.glob('run.*'):
            shutil.rmtree(dname)
        for dname in glob.glob('HYDRO_*'):
            shutil.rmtree(dname)
        for fname in ['dakota.' + ext for ext in ['dat', 'in', 'out', 'rst']]:
            if os.path.exists(fname):
                os.remove(fname)
        if os.path.exists(config_file):
            os.remove(config_file)


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@with_setup(setup, teardown)
def test_run_by_setting_attributes():
    """Test running a HydroTrend simulation."""
    if is_dakota_installed() and is_hydrotrend_installed():
        d = Dakota(method='vector_parameter_study')
        v = d.method
        v.component = 'hydrotrend'
        v.run_directory = run_dir
        v.template_file = os.path.join(data_dir, 'HYDRO.IN.tmpl')
        v.input_files = [os.path.join(data_dir, 'HYDRO0.HYPS')]
        v.variable_descriptors = ['starting_mean_annual_temperature',
                                  'total_annual_precipitation']
        v.initial_point = [10.0, 1.5]
        v.final_point = [20.0, 2.5]
        v.n_steps = 5
        v.interface = 'fork'
        v.analysis_driver = 'dakota_run_plugin'
        v.response_descriptors = ['Qs_median', 'Q_mean']
        v.response_files = ['HYDROASCII.QS', 'HYDROASCII.Q']
        v.response_statistics = ['median', 'mean']
        d.write_configuration_file(config_file)
        d.write_input_file()
        d.run()
        assert_true(os.path.exists(d.input_file))
        assert_true(os.path.exists(d.output_file))


@with_setup(setup, teardown)
def test_run_from_config_file():
    """Test running a HydroTrend simulation from a config file."""
    if is_dakota_installed() and is_hydrotrend_installed():
        d = Dakota.from_file_like(existing_config_file)
        d.method.run_directory = run_dir
        d.method.template_file = os.path.join(data_dir, 'HYDRO.IN.tmpl')
        d.method.input_files = [os.path.join(data_dir, 'HYDRO0.HYPS')]
        d.write_configuration_file(config_file)
        d.write_input_file()
        d.run()
        assert_true(os.path.exists(d.input_file))
        assert_true(os.path.exists(d.output_file))
