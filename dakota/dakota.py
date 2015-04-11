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

    def __init__(self, method=None):
        """Create a new Dakota experiment.

        Called with no parameters, a Dakota experiment with basic
        defaults (the `rosenbrock` example) is created. Use ``method``
        to set the Dakota analysis method in a new experiment.

        Parameters
        ----------
        method : str
          The desired Dakota method (e.g., `vector_parameter_study` or
          `polynomial_chaos`) to use in an experiment.

        Examples
        --------
        Create a generic Dakota experiment:

        >>> d = Dakota()

        Create a vector parameter study experiment:

        >>> d = Dakota(method='vector_parameter_study')

        """
        self.input_file = 'dakota.in'
        self.output_file = 'dakota.out'

        if method is not None:
            _module = importlib.import_module(methods_path + method)
            _class = getattr(_module, _module._classname)
            self.method = _class()
        else:
            self.method = None

    @classmethod
    def from_file_like(cls, file_like):
        """Create a Dakota instance from a file-like object.

        Parameters
        ----------
        file_like : file_like
            Input parameter file.

        Returns
        -------
        Dakota
            A new Dakota instance.

        """
        # config = yaml.load(file_like)
        # config = utils.get_configuration(file_like) # better!
        # method = config['method']
        # v = method.__class__.from_file_like(config)
        # cls.method = v # no - need class attribute
        # method = 'vector_parameter_study'
        # module = importlib.import_module(methods_path + method)
        # v = module.method()
        # cls.method = v
        return cls()

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

        Parameters
        ----------
        input_file: str, optional
          A path/name for a new Dakota input file.

        Examples
        --------
        Make an input file for a vector parameter study experiment:

        >>> d = Dakota(method='vector_parameter_study')
        >>> d.write_input_file()

        """
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
        subprocess.call(['dakota',
                         '-i', self.input_file,
                         '-o', self.output_file])
