#! /usr/bin/env python
"""Provides a Dakota interface to the HydroTrend component."""

import os
import shutil
import subprocess
import numpy as np
from .base import PluginBase
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

class HydroTrend(PluginBase):

    """Represent a HydroTrend simulation in a Dakota experiment."""

    def __init__(self, input_dir='HYDRO_IN',
                 output_dir='HYDRO_OUTPUT', input_file='HYDRO.IN',
                 input_template='HYDRO.IN.tmpl',
                 hypsometry_file='HYDRO0.HYPS', response_files=[],
                 response_statistics=[], **kwargs ):
        """Define default files and directories."""
        PluginBase.__init__(self, **kwargs)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_file = input_file
        self.input_template = input_template
        self.hypsometry_file = hypsometry_file
        self.response_files = response_files
        self.response_statistics = response_statistics
        self.response_values = []

    def setup(self, config):
        """Configure HydroTrend inputs.

        Use the Dakota parsing utility ``dprepro`` to incorporate
        parameters from Dakota into HydroTrend, creating a new
        HydroTrend input file.

        Parameters
        ----------
        config : dict
          Stores configuration settings for a Dakota experiment.

        """
        # component = config.keys()[0]
        self.input_template = config['template_file']
        self.hypsometry_file = config['input_files'][0]

        self.input_dir = os.path.join(config['run_directory'], 'HYDRO_IN')
        self.output_dir = os.path.join(config['run_directory'], 'HYDRO_OUTPUT')
        if os.path.exists(self.input_dir) is False:
            os.mkdir(self.input_dir, 0755)
        if os.path.exists(self.output_dir) is False:
            os.mkdir(self.output_dir, 0755)

        subprocess.call(['dprepro', config['parameters_file'], \
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
        for rfile, rstat in zip(self.response_files, self.response_statistics):
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
