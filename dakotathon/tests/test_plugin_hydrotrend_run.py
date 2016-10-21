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
# import filecmp
import glob
from nose.tools import with_setup, assert_true
from dakotathon.dakota import Dakota
from dakotathon.plugins.hydrotrend import is_installed \
    as is_hydrotrend_installed
from dakotathon.utils import is_dakota_installed
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

run_dir = os.getcwd()
config_file = os.path.join(run_dir, 'config.yaml')
known_config_file = os.path.join(data_dir, 'config.yaml')
# known_dat_file = os.path.join(data_dir, 'dakota.dat')

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)


def setup():
    """Called at start of any test using it @with_setup()"""
    pass


def teardown():
    """Called at end of any test using it @with_setup()"""
    if os.path.exists(config_file):
        os.remove(config_file)
    if os.path.exists('dakota.in'):
        os.remove('dakota.in')
    if is_hydrotrend_installed():
        for dname in glob.glob('HYDRO_*'):
            shutil.rmtree(dname)
    if is_dakota_installed():
        for dname in glob.glob('run.*'):
            shutil.rmtree(dname)
        for fname in ['dakota.' + ext for ext in ['dat', 'out', 'rst']]:
            if os.path.exists(fname):
                os.remove(fname)


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@with_setup(setup, teardown)
def test_run_by_setting_attributes():
    """Test running a HydroTrend simulation."""
    d = Dakota(method='vector_parameter_study', plugin='hydrotrend')
    d.template_file = os.path.join(data_dir, 'HYDRO.IN.dtmpl')
    d.auxiliary_files = os.path.join(data_dir, 'HYDRO0.HYPS')
    d.variables.descriptors = ['starting_mean_annual_temperature',
                               'total_annual_precipitation']
    d.variables.initial_point = [10.0, 1.5]
    d.method.final_point = [20.0, 2.5]
    d.method.n_steps = 5
    d.responses.response_descriptors = ['Qs_median', 'Q_mean']
    d.responses.response_files = ['HYDROASCII.QS', 'HYDROASCII.Q']
    d.responses.response_statistics = ['median', 'mean']
    d.setup()
    assert_true(os.path.exists(d.input_file))
    if is_dakota_installed() and is_hydrotrend_installed():
        d.run()
        assert_true(os.path.exists(d.output_file))
        # assert_true(filecmp.cmp(known_dat_file, d.environment.data_file))


@with_setup(setup, teardown)
def test_run_from_config_file():
    """Test running a HydroTrend simulation from a config file."""
    d = Dakota.from_file_like(known_config_file)
    d.run_directory = run_dir
    d.template_file = os.path.join(data_dir, 'HYDRO.IN.dtmpl')
    d.auxiliary_files = os.path.join(data_dir, 'HYDRO0.HYPS')
    d.serialize(config_file)
    d.write_input_file()
    assert_true(os.path.exists(d.input_file))
    if is_dakota_installed() and is_hydrotrend_installed():
        d.run()
        assert_true(os.path.exists(d.output_file))
        # assert_true(filecmp.cmp(known_dat_file, d.environment.data_file))
