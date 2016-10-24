#!/usr/bin/env python
"""Defines the `dakota_run_component` console script."""

import os
import shutil
import subprocess
import importlib
import numpy as np
from .utils import (get_configuration_file, deserialize,
                    compute_statistic, write_results)


component_script = 'dakota_run_component'
component_path = 'pymt.components'


def run_component(params_file, results_file):
    """Brokers communication between Dakota and a model through files.

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
       evaluation step, including the names and values of model
       variables and their responses. It also includes, as the
       *analysis component*, the name of a configuration file that
       stores information about the setup of the experiment, including
       the name of the model to call, input files, output file(s) to
       examine, and the statistic to apply to the output file(s).

    2. The results file contains model output values in a format
       specified by the Dakota documentation.

    Once the model is identified, an interface is created to perform
    three steps: preprocessing, execution, and postprocessing. In the
    preprocessing step, information from the configuration file is
    transferred to the component. In the execution step, the component
    is called, using the information passed from Dakota. In the
    postprocessing step, output from the component is read, and a
    single statistic (e.g., mean, median, max, etc.) is applied to
    it. This number, one for each response, is returned to Dakota
    through the results file, ending the Dakota evaluation step.

    """
    config_file = get_configuration_file(params_file)
    config = deserialize(config_file)

    try:
        module = importlib.import_module(component_path)
        cls = getattr(module, config['component'])
        component = cls()
    except (ImportError, AttributeError) as e:
        print 'Error:', e
        print 'Component cannot be created.'

    # Convert the Dakota template file to a model config file
    # with `dprepro`.
    input_file, ext = os.path.splitext(config['template_file'])
    subprocess.call(['dprepro', params_file, config['template_file'], input_file])
    shutil.copy(input_file, os.getcwd())

    # Using BMI methods, run the model and collect outputs.
    output = {}
    for key in config['response_descriptors']:
        output[key] = []
    component.initialize(input_file)
    while component.get_current_time() < component.get_end_time():
        component.update()
        for key in config['response_descriptors']:
            output[key].append(component.get_value(key))  # held in memory!
    component.finalize()
    
    # Calculate the response statistic and write the Dakota results file.
    values, labels = [], []
    for i in range(len(config['response_descriptors'])):
        descriptor = config['response_descriptors'][i]
        statistic = config['response_statistics'][i]
        r = compute_statistic(statistic, output[descriptor])
        values.append(r)
        labels.append(descriptor)
    write_results(results_file, values, labels)


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
