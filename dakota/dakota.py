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

        self.method = 'multidim_parameter_study'
        self.partitions = [8, 8]

        self.variable_type = 'continuous_design'
        self.n_variables = 2
        self.variable_descriptors = ['x1', 'x2']
        self.upper_bounds = [2.0, 2.0]
        self.lower_bounds = [-2.0, -2.0]

        self.interface = 'direct'
        self.analysis_driver = 'rosenbrock'
        self.parameters_file = 'params.in'
        self.results_file = 'results.out'

        self.n_responses = 1
        self.is_objective_function = False
        self.response_descriptors = ['r1']
        self.response_files = []
        self.response_statistics = []

    def run(self):
        """Run the specified Dakota experiment."""
        pass

    def create_input_file(self, input_file=None):
        """Create a Dakota input file on the file system."""
        if input_file is not None:
            self.input_file = input_file
        with open(self.input_file, 'w') as fp:
            fp.write(self.environment_block())
            fp.write(self.method_block())
            fp.write(self.variables_block())
            fp.write(self.interface_block())
            fp.write(self.responses_block())

    def environment_block(self):
        """Define the environment block of a Dakota input file."""
        s = '# Dakota input file\n' \
            + 'environment\n' \
            + '  tabular_data\n' \
            + '    tabular_data_file = {!r}\n\n'.format(self.data_file)
        return(s)

    def method_block(self):
        """Define the method block of a Dakota input file."""
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    partitions ='
        for p in self.partitions:
            s += ' {}'.format(p)
        s += '\n\n'
        return(s)

    def variables_block(self):
        """Define the variables block of a Dakota input file."""
        s = 'variables\n' \
            + '  {0} = {1}\n'.format(self.variable_type, self.n_variables) \
            + '    upper_bounds ='
        for b in self.upper_bounds:
            s += ' {}'.format(b)
        s += '\n' \
             + '    lower_bounds ='
        for b in self.lower_bounds:
            s += ' {}'.format(b)
        s += '\n' \
             + '    descriptors ='
        for vd in self.variable_descriptors:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)

    def interface_block(self):
        """Define the interface block of a Dakota input file."""
        s = 'interface\n' \
            + '  {}\n'.format(self.interface) \
            + '  analysis_driver = {!r}\n\n'.format(self.analysis_driver)
        return(s)

    def responses_block(self):
        """Define the responses block of a Dakota input file."""
        s = 'responses\n'
        if self.is_objective_function:
            s += '  objective_functions = {}\n'.format(self.n_responses)
        else:
            s += '  response_functions = {}\n'.format(self.n_responses)
        s += '    response_descriptors ='
        for rd in self.response_descriptors:
            s += ' {!r}'.format(rd)
        s += '\n' \
             + '  no_gradients\n' \
             + '  no_hessians\n'
        return(s)

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
