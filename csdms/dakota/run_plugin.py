#!/usr/bin/env python
"""Defines the `dakota_run_plugin` console script."""

import importlib
from .utils import get_configuration_file, get_configuration


plugin_script = 'dakota_run_plugin'
_plugins_path = 'csdms.dakota.plugins.'


def run_plugin(params_file, results_file):
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
    config = get_configuration(config_file)

    _module = importlib.import_module(_plugins_path + config['component'])
    if _module.is_installed():
        _class = getattr(_module, _module.classname)
        component = _class()
    else:
        raise NameError('Component cannot be created.')

    # Set up the simulation, call the component, calculate the
    # response statistic for the simulation, write the output to the
    # Dakota results file.
    component.setup(config)
    component.call()
    component.calculate()
    component.write(params_file, results_file)


def main():
    """Handle arguments to the `dakota_run_plugin` console script."""
    import argparse
    from . import __version__

    parser = argparse.ArgumentParser(
        description="A generic analysis driver for a Dakota experiment.")
    parser.add_argument("parameters_file",
                        help="parameters file from Dakota")
    parser.add_argument("results_file",
                        help="results file to Dakota")
    parser.add_argument('--version', action='version',
                        version=plugin_script + ' ' + __version__)
    args = parser.parse_args()

    run_plugin(args.parameters_file, args.results_file)

if __name__ == '__main__':
    main()
