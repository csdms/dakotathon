#! /usr/bin/env python
"""Provides a Dakota interface to the HydroTrend component."""

import os
import shutil
import subprocess
import numpy as np
from .base import PluginBase
from csdms.dakota.utils import get_response_descriptors, write_results, \
    compute_statistic


classname = 'HydroTrend'


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
                 hypsometry_file='HYDRO0.HYPS', output_files=None,
                 output_statistics=None, **kwargs):
        """Define default files and directories."""
        PluginBase.__init__(self, **kwargs)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_file = input_file
        self.input_template = input_template
        self.hypsometry_file = hypsometry_file
        self.output_files = output_files
        self.output_statistics = output_statistics
        self.output_values = []

    def setup(self, config):
        """Configure HydroTrend inputs.

        Sets attributes using information from the run configuration
        file. The Dakota parsing utility ``dprepro`` reads parameters
        from Dakota to create a new HydroTrend input file from a
        template.

        Parameters
        ----------
        config : dict
          Stores configuration settings for a Dakota experiment.

        """
        self.setup_files(config)
        self.setup_directories(config)
        subprocess.call(['dprepro', config['parameters_file'],
                         self.input_template,
                         self.input_file])
        shutil.copy(self.input_file, self.input_dir)
        shutil.copy(self.hypsometry_file, self.input_dir)

    def setup_files(self, config):
        """Configure HydroTrend input and output files.

        Parameters
        ----------
        config : dict
          Configuration settings for a Dakota experiment.

        """
        self.input_template = config['template_file']
        self.hypsometry_file, = config['input_files']
        self.output_files = config['response_files']
        self.output_statistics = config['response_statistics']

    def setup_directories(self, config):
        """Configure HydroTrend input and output directories.

        Parameters
        ----------
        config : dict
          Configuration settings for a Dakota experiment.

        """
        # self.input_dir = os.path.join(config['run_directory'], 'HYDRO_IN')
        # self.output_dir = os.path.join(config['run_directory'], 'HYDRO_OUTPUT')
        self.input_dir = os.path.join('..', 'HYDRO_IN')
        self.output_dir = os.path.join('..', 'HYDRO_OUTPUT')
        if os.path.exists(self.input_dir) is False:
            os.mkdir(self.input_dir, 0755)
        if os.path.exists(self.output_dir) is False:
            os.mkdir(self.output_dir, 0755)

    def call(self):
        """Invoke HydroTrend through the shell."""
        subprocess.call(['hydrotrend',
                         '--in-dir', self.input_dir,
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
        """Calculate Dakota output functions."""
        for rfile, rstat in zip(self.output_files, self.output_statistics):
            shutil.copy(os.path.join(self.output_dir, rfile), os.curdir)
            series = self.load(rfile)
            if series is not None:
                val = compute_statistic(rstat, series)
                self.output_values.append(val)
            else:
                self.output_values.append(float('nan'))

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
        write_results(results_file, self.output_values, labels)

    @staticmethod
    def write_tmpl_file(base_tmpl_file, base_input_file, parameter_names):
        """Create a template HydroTrend input file used by Dakota.

        The tmpl file is a HydroTrend input file, but with the
        parameters used by Dakota replaced with their descriptors set
        in the Dakota input file. The tmpl file is written to the
        current directory.

        Parameters
        ----------
        base_tmpl_file : str
          The path to the template file defined for the HydroTrend
          component.
        base_input_file : str
          A HydroTrend input file that contains parameter values for a
          HydroTrend simulation.
        parameter_names : list of str
          A list of HydroTrend parameter names (standard names) that
          will be evaluated by Dakota.

        Returns
        -------
        str or None
          The path to the new tmpl file, or None on an error.

        """
        import re

        with open(base_tmpl_file, 'r') as fp:
            txt_base_tmpl = fp.read().split('\n')
        with open(base_input_file, 'r') as fp:
            txt_base_input = fp.read().split('\n')

        if len(txt_base_tmpl) != len(txt_base_input):
            raise

        for p_name in parameter_names:
            for i, line_tmpl in enumerate(txt_base_tmpl):
                if re.search(p_name, line_tmpl):
                    line_input = txt_base_input[i]
                    line_tmpl_split = line_tmpl.strip().split()
                    line_input_split = line_input.strip().split()
                    for j, item in enumerate(line_tmpl_split):
                        if item.startswith('{' + p_name):
                            line_input_split[j] = '{' + p_name + '}'
                    txt_base_input[i] = ' '.join(line_input_split)

        tmpl_file = 'HYDRO.IN.tmpl'
        with open(tmpl_file, 'w') as fp:
            fp.write('\n'.join(txt_base_input))
            return tmpl_file
