#! /usr/bin/env python
"""Interface to the Dakota iterative systems analysis toolkit."""

import subprocess


class Dakota(object):
    """Describe and run a Dakota experiment."""

    def __init__(self):
        """Create a new Dakota experiment with default parameters."""
        self.input_file = 'dakota.in'
        self.output_file = 'dakota.out'
        self.data_file = 'dakota.dat'

        self.method = None

        self.variable_type = 'continuous_design'
        self.n_variables = 0
        self.variable_descriptors = []

        self.analysis_driver = None

        self.n_responses = 0
        self.response_descriptors = []

    def run(self):
        """Run the specified Dakota experiment."""
        print(self.method)
        print(self.variable_type + " = " + str(self.n_variables))

    def write(self):
        """Write a Dakota input file."""
        pass
