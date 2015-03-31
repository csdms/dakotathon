
#! /usr/bin/env python
"""Interface to the Dakota iterative systems analysis toolkit."""

import subprocess


class Dakota(object):
    """Describe and run a Dakota experiment."""

    def __init__(self):
        """Create a new Dakota experiment with default parameters."""
        self.model = None
        self.input_file = 'dakota.in'
        self.output_file = 'dakota.out'
        self.data_file = 'dakota.dat'

        self.method = None

        self.variable_type = 'continuous_design'
        self.n_variables = 0
        self.variable_descriptors = []

        self.analysis_driver = 'run_model.py'
        self.parameters_file = 'params.in'
        self.results_file = 'results.out'

        self.n_responses = 0
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

def write_results(results_file, array, labels):
    """Write a Dakota results file from an input numpy array."""
    try:
        with open(results_file, 'w') as fp:
            for i in range(len(array)):
                fp.write('{0s}\t{1}\n'.format(array[i], labels[i]))
    except IOError:
        raise
