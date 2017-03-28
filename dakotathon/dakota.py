#! /usr/bin/env python
"""A Python interface to the Dakota iterative systems analysis toolkit."""

import os
import subprocess
import types
import yaml
from .experiment import Experiment


class Dakota(Experiment):

    """Controller for configuring and running a Dakota experiment."""

    def __init__(self,
                 run_directory=os.getcwd(),
                 configuration_file='dakota.yaml',
                 input_file='dakota.in',
                 output_file='dakota.out',
                 template_file=None,
                 auxiliary_files=(),
                 **kwargs):
        """Initialize a Dakota experiment.

        Called with no parameters, a Dakota experiment with basic defaults
        (a vector parameter study with the built-in `rosenbrock` example)
        is created. Use ``method`` to set the Dakota analysis method in a
        new experiment.

        Parameters
        ----------
        run_directory : str, optional
            The working directory in which Dakota is run, and output
            is placed (default is the current directory).
        configuration_file : str, optional
            A Dakota instance serialized to a YAML file (default is
            **dakota.yaml**).
        input_file : str, optional
            Name of Dakota input file (default is **dakota.in**)
        output_file : str, optional
            Name of Dakota output file (default is **dakota.out**)
        template_file : str, optional
            The Dakota template file, formed from the input file of
            the model to study, but with study variables replaced by
            descriptors in braces; e.g., ``{total_annual_precipitation}``
            (default is None).
        auxiliary_files : str or tuple or list of str, optional
            Additional input files used by the model being studied.
        **kwargs
            Arbitrary keyword arguments.

        Examples
        --------
        Create a generic Dakota experiment:

        >>> d = Dakota()

        Create a vector parameter study experiment:

        >>> d = Dakota(method='vector_parameter_study')

        """
        Experiment.__init__(self, **kwargs)
        configuration_file = os.path.abspath(os.path.join(run_directory, configuration_file))
        self._run_directory = run_directory
        self._configuration_file = configuration_file
        self.input_file = input_file
        self.output_file = output_file
        self._template_file = template_file
        self._auxiliary_files = auxiliary_files

    @property
    def run_directory(self):
        """The run directory path."""
        return self._run_directory

    @run_directory.setter
    def run_directory(self, value):
        """Set the run directory path.

        Parameters
        ----------
        value : str
          The new run directory path (default is current directory).

        """
        self._run_directory = os.path.abspath(value)

    @property
    def configuration_file(self):
        """The configuration file path."""
        return self._configuration_file

    @configuration_file.setter
    def configuration_file(self, value):
        """Set the configuration file path.

        Parameters
        ----------
        value : str
          The new file path (default is 'dakota.yaml').

        """
        if not os.path.isabs(value):
            value = os.path.abspath(value)
        self._configuration_file = value
        if self.interface.interface == 'fork':
            self.interface._configuration_file = value

    @property
    def template_file(self):
        """The template file path."""
        return self._template_file

    @template_file.setter
    def template_file(self, value):
        """Set the template file path.

        Parameters
        ----------
        value : str
          The new file path.

        """
        if value is not None:
            if not os.path.isabs(value):
                value = os.path.abspath(value)
        self._template_file = value

    @property
    def auxiliary_files(self):
        """Auxiliary files used by the component."""
        return self._auxiliary_files

    @auxiliary_files.setter
    def auxiliary_files(self, value):
        """Set the auxiliary files used by component.

        Parameters
        ----------
        value : str or list or tuple of str
          The new auxiliary file(s).

        """
        files = []
        if type(value) is str:
            value = [value]
        if not isinstance(value, (tuple, list)):
            raise TypeError("Input files must be a string, tuple or list")
        for item in value:
            files.append(os.path.abspath(item))
        self._auxiliary_files = tuple(files)

    @classmethod
    def from_file_like(cls, file_like):
        """Create a Dakota instance from a file-like object.

        Parameters
        ----------
        file_like : file_like
            A configuration file or file-like object.

        Returns
        -------
        Dakota
            A new Dakota instance.

        """
        config = {}
        if isinstance(file_like, types.StringTypes):
            with open(file_like, 'r') as fp:
                config = yaml.load(fp.read())
        else:
            config = yaml.load(file_like)
        return cls(**config)

    def serialize(self, config_file=None):
        """Dump settings for experiment to a YAML configuration file.

        Parameters
        ----------
        config_file : str, optional
          A path/name for a new configuration file.

        Examples
        --------
        Make a configuration file for a vector parameter study
        experiment:

        >>> d = Dakota(method='vector_parameter_study')
        >>> d.serialize('dakota.yaml')

        """
        from .utils import get_attributes

        if config_file is not None:
            self.configuration_file = config_file

        props = get_attributes(self)
        
        removed_blocks = set(Experiment.blocks)-set(self.blocks)
        for removed_block in removed_blocks:
            temp = props.pop(removed_block)
            del temp
        
        for section in self.blocks:
            section_props = get_attributes(props.pop(section))
            props = dict(list(props.items()) + list(section_props.items()))

        with open(self.configuration_file, 'w') as fp:
            yaml.safe_dump(props, fp, default_flow_style=False)

    def write_input_file(self, input_file=None):
        """Create the Dakota input file for the experiment.

        The input file is written to the directory specified by the
        `run_directory` attribute.

        Parameters
        ----------
        input_file : str, optional
          A path/name for a new Dakota input file.

        Examples
        --------
        Make an input file for a vector parameter study experiment:

        >>> d = Dakota(method='vector_parameter_study')
        >>> d.write_input_file('dakota.in')

        """
        if input_file is not None:
            self.input_file = input_file
        
        input_file_path = os.path.abspath(os.path.join(self.run_directory,
                                                        self.input_file))
        with open(input_file_path, 'w') as fp:
            fp.write(str(self))

    def setup(self):
        """Write the Dakota configuration and input files.

        Examples
        --------
        As a convenience, make a configuration file and an input file
        for an experiment in one step:

        >>> d = Dakota(method='vector_parameter_study')
        >>> d.setup()

        """
        self.serialize()
        self.write_input_file()

    def run(self):
        """Run the Dakota experiment."""
        os.chdir(self.run_directory)

        subprocess.check_output(['dakota',
                                 '-i', self.input_file,
                                 '-o', self.output_file],
                                stderr=subprocess.STDOUT) 

