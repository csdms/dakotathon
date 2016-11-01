#!/usr/bin/env python
"""Defines the `dakota_run_component` console script."""

import os
import shutil
import subprocess
import importlib
import numpy as np
from .utils import (get_configuration_file, deserialize,
                    compute_statistic, write_results, to_iterable)


component_script = 'dakota_run_component'


class ComponentOutput(object):

    """Stores component output variables for processing by Dakota."""

    def __init__(self, component, var_names):
        self.component = component
        self.var_names = to_iterable(var_names)
        for var in self.var_names:
            setattr(self, var, [])

    def update(self):
        for var in self.var_names:
            attr = getattr(self, var)
            attr.append(self.component.get_value(var))

    def get_value(self, var):
        return getattr(self, var)


class RunComponent(object):

    """Provides framework to run a CSDMS component from Dakota."""

    component_path = 'pymt.components'

    def __init__(self, params_file, results_file):
        self.params_file = params_file
        self.results_file = results_file
        self.component = None
        self.output = None
        self.results = []

        config_file = get_configuration_file(self.params_file)
        self.config = deserialize(config_file)

    def create_component(self):
        module = importlib.import_module(self.component_path)
        cls = getattr(module, self.config['component'])
        self.component = cls()

    def setup(self):
        shutil.copy(os.path.join(self.config['run_directory'],
                                 self.config['template_file']), os.getcwd())
        input_file, _ = os.path.splitext(self.config['template_file'])
        subprocess.call(['dprepro', self.params_file,
                         self.config['template_file'],
                         input_file])
        for fname in self.config['auxiliary_files']:
            shutil.copy(os.path.join(self.config['run_directory'], fname), os.getcwd())
        self.output = ComponentOutput(self.component,
                                      self.config['response_descriptors'])

    def run(self):
        self.component.initialize(self.config['initialize_args'])
        while self.component.get_current_time() < self.component.get_end_time():
            self.component.update()
            self.output.update()
        self.component.finalize()

    def calculate(self):
        for i in range(len(self.config['response_descriptors'])):
            desc = self.config['response_descriptors'][i]
            stat = self.config['response_statistics'][i]
            r = compute_statistic(stat, self.output.get_value(desc))
            self.results.append(r)

    def write(self):
        write_results(self.results_file, self.results,
                      self.config['response_descriptors'])


def run_component(params_file, results_file):
    """Brokers communication between Dakota and a CSDMS component.

    Parameters
    ----------
    params_file : str
      The path to the parameters file created by Dakota.
    results_file : str
      The path the results file returned to Dakota.

    Notes
    -----
    This console script provides a generic *analysis driver* for a
    Dakota experiment. At each evaluation step, Dakota calls this
    script with two arguments, the names of the parameters and results files:

    1. The parameters file provides information on the current Dakota
       evaluation step, including the names and values of component
       variables and their responses. It also includes, as the
       *analysis component*, the name of a configuration file that
       stores information about the setup of the experiment, including
       the name of the component to call, input files, output file(s) to
       examine, and the statistic to apply to the output file(s).

    2. The results file contains component output values in a format
       specified by the Dakota documentation.

    Once the component is identified, a worker is created to perform
    three steps: preprocessing, execution, and postprocessing. In the
    preprocessing step, information from the configuration file is
    transferred to the component. In the execution step, the component
    is called, using the information passed from Dakota. In the
    postprocessing step, output from the component is read, and a
    single statistic (e.g., mean, median, max, etc.) is applied to
    it. This number, one for each response, is returned to Dakota
    through the results file, ending the Dakota evaluation step.

    """
    runner = RunComponent(params_file, results_file)
    runner.create_component()
    runner.setup()
    runner.run()
    runner.calculate()
    runner.write()


def main():
    """Handle arguments to the `dakota_run_component` console script."""
    import argparse
    from . import __version__

    parser = argparse.ArgumentParser(
        description="A generic analysis driver for a Dakota experiment.")
    parser.add_argument("parameters_file",
                        help="parameters file from Dakota")
    parser.add_argument("results_file",
                        help="results file to Dakota")
    parser.add_argument('--version', action='version',
                        version=component_script + ' ' + __version__)
    args = parser.parse_args()

    run_component(args.parameters_file, args.results_file)

if __name__ == '__main__':
    main()
