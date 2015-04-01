#! /usr/bin/env python
"""Interface to the Dakota iterative systems analysis toolkit."""

import subprocess
import re

class Dakota(object):
    """Describe and run a Dakota experiment."""

    def __init__(self):
        """Create a new Dakota experiment with default parameters."""
        self.model = None
        self.input_file = 'dakota.in'
        self.output_file = 'dakota.out'
        self.data_file = 'dakota.dat'

        self.method = 'vector_parameter_study'
        self.final_point = [1.1, 1.3]
        self.initial_point = [-0.3, 0.2]
        self.n_steps = 10

        self.variable_type = 'continuous_design'
        self.n_variables = 2
        self.variable_descriptors = ['x1', 'x2']

        self.interface = 'direct'
        self.analysis_driver = 'rosenbrock'
        self.parameters_file = 'params.in'
        self.results_file = 'results.out'

        self.n_response_functions = 0
        self.n_objective_functions = 1
        self.response_descriptors = []
        self.response_files = []
        self.response_statistics = []

    def run(self):
        """Run the specified Dakota experiment."""
        print(self.method)
        print(self.analysis_driver)

    def write(self):
        """Write a Dakota input file."""
        pass

def get_labels(params_file):
    """Extract labels from a Dakota parameters file."""
    labels = []
    try:
        with open(params_file, 'r') as fp:
            for line in fp:
                if re.search('ASV_', line):
                    labels.append(''.join(re.findall(':(\S+)', line)))
    except IOError:
        return None
    else:
        return(labels)

def get_analysis_components(params_file):
    """Extract the analysis components from a Dakota parameters file.

    The analysis components are returned as a list. First is the name
    of the model being run by Dakota, followed by dicts containing an
    output file to analyze and the statistic to apply to the file.

    Parameters
    ----------
    params_file : str
      The path to a Dakota parameters file.

    Returns
    -------
    list
      A list of analysis components for the Dakota experiment.

    Examples
    --------
    Extract the analysis components from a Dakota parameters file:

    >>> ac = get_analysis_components(params_file)
    >>> ac.pop(0)
    'hydrotrend'
    >>> ac.pop(0)
    {'file': 'HYDROASCII.QS', 'statistic': 'median'}

    Notes
    -----
    The syntax expected by this function is defined in the Dakota
    input file; e.g., for the example cited above, the 'interface'
    section of the input file contains the line:

      analysis_components = 'hydrotrend' 'HYDROASCII.QS:median'

    """
    ac = []
    try:
        with open(params_file, 'r') as fp:
            for line in fp:
                if re.search('AC_1', line):
                    ac.append(line.split('AC_1')[0].strip())
                elif re.search('AC_', line):
                    parts = re.split(':', re.split('AC_', line)[0])
                    ac.append({'file':parts[0].strip(),
                               'statistic':parts[1].strip()})
    except IOError:
        return None
    else:
        return(ac)    

def write_results(results_file, array, labels):
    """Write a Dakota results file from an input numpy array."""
    try:
        with open(results_file, 'w') as fp:
            for i in range(len(array)):
                fp.write('{0s}\t{1}\n'.format(array[i], labels[i]))
    except IOError:
        raise
