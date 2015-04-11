#! /usr/bin/env python
"""Provides a Dakota interface to the HydroTrend component."""

import os
import shutil
import subprocess
import numpy as np
from dakota.utils import get_response_descriptors, write_results, \
    compute_statistic


_classname = 'HydroTrend'

def is_installed():
    """Check whether HydroTrend is in the execution path."""
    try:
        subprocess.call(['hydrotrend', '--version'])
    except OSError:
        return False
    else:
        return True

class HydroTrend(object):

    """Represent a HydroTrend simulation in a Dakota experiment."""

    def __init__(self):
        """Define default files and directories."""
        self.input_dir = 'HYDRO_IN'
        self.output_dir = 'HYDRO_OUTPUT'
        self.input_file = 'HYDRO.IN'
        self.input_template = 'HYDRO.IN.tmpl'
        self.hypsometry_file = 'HYDRO0.HYPS'
        self.response_functions = []
        self.response_values = []

    def setup(self, config, params_file):
        """Configure HydroTrend inputs.

        Use the Dakota parsing utility ``dprepro`` to incorporate
        parameters from Dakota into HydroTrend, creating a new
        HydroTrend input file.

        Parameters
        ----------
        config : dict
          Stores configuration settings for a Dakota experiment.
        params_file : str
          The path to a Dakota parameters file.

        """
        component = config.keys()[0]
        self.input_template = config[component]['template_file']
        self.hypsometry_file = config[component]['input_files'][0]
        self.response_functions = config[component]['responses']
        start_dir = config[component]['run_directory']

        self.input_dir = os.path.join(start_dir, 'HYDRO_IN')
        self.output_dir = os.path.join(start_dir, 'HYDRO_OUTPUT')
        if os.path.exists(self.input_dir) is False:
            os.mkdir(self.input_dir, 0755)
        if os.path.exists(self.output_dir) is False:
            os.mkdir(self.output_dir, 0755)

        subprocess.call(['dprepro', params_file, \
                         self.input_template, \
                         self.input_file])
        shutil.copy(self.input_file, self.input_dir)
        shutil.copy(self.hypsometry_file, self.input_dir)

    def call(self):
        """Invoke HydroTrend through the shell."""
        subprocess.call(['hydrotrend', \
                         '--in-dir', self.input_dir, \
                         '--out-dir', self.output_dir])

    def load(self, output_file):
        """Read a column of data from a HydroTrend output file.

        Parameters
        ----------
        output_file : str
          The path to a text HydroTrend output file.

        Returns
        -------
        array_like
          A numpy array, or None on an error.
        
        """
        try:
            series = np.loadtxt(output_file, skiprows=2)
        except (IOError, StopIteration):
            return(None)
        else:
            return(series)

    def calculate(self):
        """Calculate Dakota response functions."""
        for response in self.response_functions:
            rfile = response.keys()[0]
            rstat = response.values()[0]
            shutil.copy(os.path.join(self.output_dir, rfile), os.curdir)
            series = self.load(rfile)
            if series is not None:
                val = compute_statistic(rstat, series)
                self.response_values.append(val)
            else:
                self.response_values.append(float('nan'))


    def write(self, params_file, results_file):
        """Write the Dakota results file.

        Parameters
        ----------
        params_file : str
          A Dakota parameters file.
        results_file : str
          A Dakota results file.

        """
        labels = get_response_descriptors(params_file)
        write_results(results_file, self.response_values, labels)
