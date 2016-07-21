"""A template for describing a Dakota experiment."""

import os
import importlib
import inspect


class Experiment(object):

    """Describe the features of a Dakota experiment."""

    def __init__(self,
                 method='vector_parameter_study',
                 variables='continuous_design',
                 interface='direct',
                 responses='response_functions',
                 component=None,
                 run_directory=os.getcwd(),
                 template_file=None,
                 input_files=(),
                 **kwargs):
        """Create a set of default experiment parameters."""
        self.component = component
        self._run_directory = run_directory
        self._configuration_file = os.path.abspath('config.yaml')
        self._template_file = template_file
        self.input_files = input_files

        self.environment = self._import('environment', 'environment', **kwargs)
        self.method = self._import('method', method, **kwargs)
        self.variables = self._import('variables', variables, **kwargs)
        if self.component is not None:
            interface = 'fork'
        self.interface = self._import('interface', interface, **kwargs)
        self.responses = self._import('responses', responses, **kwargs)

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
          The new file path.

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

    @classmethod
    def from_file_like(cls, file_like):
        """Create a new Experiment from a file-like object.

        Parameters
        ----------
        file_like : file_like
            Input parameter file.

        Returns
        -------
        Experiment
            A new Experiment.

        """
        config = {}
        if isinstance(file_like, types.StringTypes):
            with open(file_like, 'r') as fp:
                config = yaml.load(fp.read())
        else:
            config = yaml.load(file_like)
        return cls(**config)

    def _get_subpackage_namespace(self, subpackage):
        return os.path.splitext(self.__module__)[0] + '.' + subpackage

    def _import(self, subpackage, module, **kwargs):
        namespace = self._get_subpackage_namespace(subpackage) + '.' + module
        module = importlib.import_module(namespace)
        cls = getattr(module, module.classname)
        return cls(**kwargs)

    def __str__(self):
        s = str(self.environment) \
            + str(self.method) \
            + str(self.variables) \
            + str(self.interface) \
            + str(self.responses)
        return s
