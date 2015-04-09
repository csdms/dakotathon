#! /usr/bin/env python
"""Interface to the Dakota iterative systems analysis toolkit."""

import os
import subprocess
import importlib
import yaml
from .utils import is_dakota_installed
from . import methods_path


class Dakota(object):

    """Set up and run a Dakota experiment."""

    def __init__(self, input_file=None, method=None):
        """Create a new Dakota experiment.

        One of either ``input_file`` or ``method`` is required, and
        they're exclusive. Use ``input_file`` to run Dakota with an
        existing input file. Use ``method`` to configure a new
        experiment and create a new input file.

        Parameters
        ----------
        input_file: str
          The path to a Dakota input file.
        method : str
          The desired Dakota method (e.g., `vector_parameter_study` or
          `polynomial_chaos`) to use in an experiment.

        Examples
        --------
        Create a Dakota experiment from an existing input file:

        >>> d = Dakota(input_file='/path/to/dakota.in')

        Configure a vector parameter study experiment:

        >>> d = Dakota(method='vector_parameter_study')
        >>> d.write_input_file()

        """
        if [input_file, method].count(None) != 1:
            raise TypeError('Must specify exactly one input file or method.')

        self.input_file = 'dakota.in'
        self.output_file = 'dakota.out'

        if input_file is not None:
            self.input_file = input_file
        else:
            module = importlib.import_module(methods_path + method)
            self.method = module.method()

    def write_configuration_file(self):
        """Dump settings to a YAML configuration file."""
        responses = []
        for f,s in zip(self.method.response_files,
                       self.method.response_statistics):
            responses.append({f:s})
        config = {self.method.component:
                  {
                      'run_directory': self.method.run_directory,
                      'template_file': self.method.template_file,
                      'input_files': self.method.input_files,
                      'responses': responses
                  }
              }
        with open(self.method.configuration_file, 'w') as fp:
            yaml.dump(config, fp, default_flow_style=False)

    def write_input_file(self, input_file=None):
        """Create a Dakota input file on the file system.

        Only instances created with ``method`` can create a new Dakota
        input file.

        Parameters
        ----------
        input_file: str, optional
          A path/name for a new Dakota input file.

        """
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
        if is_dakota_installed() is False:
            raise OSError('Dakota must be installed and in execution path.')
        if os.path.exists(self.input_file) is False:
            raise IOError('Dakota input file not found.')
        else:
            subprocess.call(['dakota',
                             '-i', self.input_file,
                             '-o', self.output_file])

