#! /usr/bin/env python
"""Interface to the Dakota iterative systems analysis toolkit."""

import os
import subprocess
import importlib


class Dakota(object):
    """Set up and run a Dakota experiment."""

    def __init__(self, input_file=None, method=None):
        """Create a new Dakota experiment."""
        if [input_file, method].count(None) != 1:
            raise TypeError('Must specify exactly one input file or method.')

        self.input_file = 'dakota.in'
        self.output_file = 'dakota.out'

        if input_file is not None:
            self.input_file = input_file
        else:
            module = importlib.import_module('dakota.' + method)
            self.method = module.method()

    def create_input_file(self, input_file=None):
        """Create a Dakota input file on the file system."""
        if hasattr(self, 'method') is False:
            raise TypeError('Instance created with `input_file` is read-only.')
        if input_file is not None:
            self.input_file = input_file
        with open(self.input_file, 'w') as fp:
            fp.write(self.method.environment_block())
            fp.write(self.method.method_block())
            fp.write(self.method.variables_block())
            fp.write(self.method.interface_block())
            fp.write(self.method.responses_block())

    def run(self):
        """Run the Dakota experiment."""
        if os.path.exists(self.input_file) is False:
            raise IOError('Dakota input file not found.')
        else:
            r = subprocess.call(['dakota',
                                 '-i', self.input_file,
                                 '-o', self.output_file])

