#! /usr/bin/env python
"""An abstract base class for all Dakota analysis methods."""

from abc import ABCMeta, abstractmethod
import os
import types
import yaml


class MethodsBase(object):

    """Describe features common to all Dakota analysis methods."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 component=None,
                 method=None,
                 configuration_file=os.path.abspath('config.yaml'),
                 run_directory=os.getcwd(),
                 template_file=None,
                 input_files=(),
                 data_file='dakota.dat',
                 variable_type='continuous_design',
                 variables=(),
                 interface='direct',
                 id_interface='CSDMS',
                 analysis_driver='rosenbrock',
                 is_objective_function=False,
                 response_descriptors=(),
                 response_files=(),
                 response_statistics=(),
                 **kwargs):
        """Create a set of default experiment parameters."""
        self.component = component
        self._run_directory = run_directory
        self._configuration_file = configuration_file
        self._template_file = template_file
        self.input_files = input_files
        self.data_file = data_file
        self.method = method
        self.variable_type = variable_type
        self._variables = variables
        self.interface = interface
        self.id_interface = id_interface
        self.analysis_driver = analysis_driver
        self.parameters_file = 'params.in'
        self.results_file = 'results.out'
        self.is_objective_function = is_objective_function
        self._response_descriptors = response_descriptors
        self._response_files = response_files
        self._response_statistics = response_statistics

        if self.component is not None:
            if self.analysis_driver == 'rosenbrock':
                self.analysis_driver = 'dakota_run_plugin'
            if self.interface == 'direct':
                self.interface = 'fork'

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
          The new run directory path.

        """
        if not os.path.isabs(value):
            value = os.path.abspath(value)
        self._run_directory = value

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
          The new file path.

        """
        if not os.path.isabs(value):
            value = os.path.abspath(value)
        self._configuration_file = value

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
    def input_files(self):
        """A tuple of input files used by the component."""
        return self._input_files

    @input_files.setter
    def input_files(self, value):
        """Set input files used by component.

        Parameters
        ----------
        value : str or list or tuple of str
          The new input file(s).

        """
        input_files = []
        if type(value) is str:
            value = [value]
        if not isinstance(value, (tuple, list)):
            raise TypeError("Input files must be a string, tuple or list")
        for item in value:
            input_files.append(os.path.abspath(item))
        self._input_files = tuple(input_files)

    @property
    def variables(self):
        """Labels attached to Dakota variables."""
        return self._variables

    @variables.setter
    def variables(self, value):
        """Set labels for Dakota variables.

        Parameters
        ----------
        value : list or tuple of str
          The new variables labels.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Descriptor must be a tuple or a list")
        self._variables = value

    @property
    def response_descriptors(self):
        """Labels attached to Dakota responses."""
        return self._response_descriptors

    @response_descriptors.setter
    def response_descriptors(self, value):
        """Set labels for Dakota responses.

        Parameters
        ----------
        value : list or tuple of str
          The new response labels.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Descriptor must be a tuple or a list")
        self._response_descriptors = value

    @property
    def response_files(self):
        """Model output files used in Dakota responses."""
        return self._response_files

    @response_files.setter
    def response_files(self, value):
        """Set model output files for Dakota responses.

        Parameters
        ----------
        value : list or tuple of str
          The new response files.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Response files must be a tuple or a list")
        self._response_files = value

    @property
    def response_statistics(self):
        """Model output statistics used in Dakota responses."""
        return self._response_statistics

    @response_statistics.setter
    def response_statistics(self, value):
        """Set model output statistics for Dakota responses.

        Parameters
        ----------
        value : list or tuple of str
          The new response statistics.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Response statistics must be a tuple or a list")
        self._response_statistics = value

    @classmethod
    def from_file_like(cls, file_like):
        """Create a MethodsBase instance from a file-like object.

        Parameters
        ----------
        file_like : file_like
            Input parameter file.

        Returns
        -------
        MethodsBase
            A new MethodsBase instance.

        """
        config = {}
        if isinstance(file_like, types.StringTypes):
            with open(file_like, 'r') as fp:
                config = yaml.load(fp.read())
        else:
            config = yaml.load(file_like)
        return cls(**config)

    def environment_block(self):
        """Define the environment block of a Dakota input file."""
        s = '# Dakota input file\n' \
            + 'environment\n' \
            + '  tabular_data\n' \
            + '    tabular_data_file = {!r}\n\n'.format(self.data_file)
        return(s)

    @abstractmethod
    def method_block(self):
        """Define the method block of a Dakota input file."""
        s = 'method\n' \
            + '  {}\n\n'.format(self.method)
        return(s)

    def variables_block(self):
        """Define the variables block of a Dakota input file."""
        s = 'variables\n' \
            + ' {0} = {1}\n'.format(self.variable_type,
                                    len(self.variables))
        s += '    descriptors ='
        for vd in self.variables:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)

    def interface_block(self):
        """Define the interface block of a Dakota input file."""
        s = 'interface\n' \
            + '  id_interface = {!r}\n'.format(self.id_interface) \
            + '  {}\n'.format(self.interface) \
            + '  analysis_driver = {!r}\n'.format(self.analysis_driver)
        if self.component is not None:
            s += '  analysis_components = {!r}\n'.format(self.configuration_file)
        if self.interface is not 'direct':
            s += '  parameters_file = {!r}\n'.format(self.parameters_file) \
                 + '  results_file = {!r}\n'.format(self.results_file) \
                 + '  work_directory\n' \
                 + '    named \'run\'\n' \
                 + '    directory_tag\n' \
                 + '    directory_save\n' \
                 + '  file_save\n'
        s += '\n'
        return(s)

    def responses_block(self):
        """Define the responses block of a Dakota input file."""
        n_responses = len(self.response_descriptors)
        s = 'responses\n'
        if self.is_objective_function:
            s += '  objective_functions = {}\n'.format(n_responses)
        else:
            s += '  response_functions = {}\n'.format(n_responses)
        s += '    response_descriptors ='
        for rd in self.response_descriptors:
            s += ' {!r}'.format(rd)
        s += '\n' \
             + '  no_gradients\n' \
             + '  no_hessians\n'
        return(s)
