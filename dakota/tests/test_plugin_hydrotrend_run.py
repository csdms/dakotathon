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
from nose.tools import *
from dakota.dakota import Dakota
from dakota.plugins.hydrotrend import is_installed as is_hydrotrend_installed
from dakota.utils import is_dakota_installed
from . import start_dir, data_dir


# Global variables -----------------------------------------------------

component = 'hydrotrend'
config_file = 'config.yaml'
template_file = 'HYDRO.IN.tmpl'
hypsometry_file = 'HYDRO0.HYPS'
analysis_driver = 'dakota_run_plugin'

# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)

def setup():
    """Called at start of any test using it @with_setup()"""
    if is_dakota_installed():
        global d
        d = Dakota(method='vector_parameter_study')
        v = d.method
        v.component = component
        v.run_directory = os.getcwd()
        v.configuration_file = os.path.join(v.run_directory, config_file)
        v.template_file = os.path.join(data_dir, template_file)
        v.input_files = [os.path.join(data_dir, hypsometry_file)]
        v.variable_descriptors = ['starting_mean_annual_temperature',
                                  'total_annual_precipitation']
        v.n_variables = len(v.variable_descriptors)
        v.initial_point = [10.0, 1.5]
        v.final_point = [20.0, 2.5]
        v.n_steps = 5
        v.interface = 'fork'
        v.analysis_driver = analysis_driver
        v.response_descriptors = ['Qs_median', 'Q_mean']
        v.n_responses = len(v.response_descriptors)
        v.response_files = ['HYDROASCII.QS', 'HYDROASCII.Q']
        v.response_statistics = ['median', 'mean']
        d.write_configuration_file()
        d.write_input_file()

def teardown():
    """Called at end of any test using it @with_setup()"""
    if is_dakota_installed():
        for dname in glob.glob('run.*'):
            shutil.rmtree(dname)
        for dname in glob.glob('HYDRO_*'):
            shutil.rmtree(dname)
        for fname in ['dakota.' + ext for ext in ['dat', 'in', 'out', 'rst']]:
            os.remove(fname)
        os.remove(config_file)

def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------

@with_setup(setup, teardown)
def test_run():
    """Test running a HydroTrend simulation."""
    if is_dakota_installed() and is_hydrotrend_installed():
        d.run()
        assert_true(os.path.exists(d.input_file))
        assert_true(os.path.exists(d.output_file))
