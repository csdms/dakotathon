"""A Python interface to a Dakota input file."""

import os
import importlib


class Experiment(object):

    """An aggregate of control blocks that define a Dakota input file."""

    blocks = ('environment', 'method', 'variables', 'interface', 'responses')
    """The named control blocks of a Dakota input file."""

    def __init__(self,
                 component=None,
                 environment='environment',
                 method='vector_parameter_study',
                 variables='continuous_design',
                 interface='direct',
                 responses='response_functions',
                 **kwargs):
        """Create the set of control blocks for a Dakota experiment.

        Called with no parameters, a Dakota experiment with basic defaults
        (a vector parameter study with the built-in `rosenbrock` example)
        is created.

        Parameters
        ----------
        component : str, optional
            Name of CSDMS component which Dakota is analyzing (default
            is None).
        environment : str, optional
            Type of environment used in Dakota experiment (default is
            'environment').
        method : str, optional
            Type of method used in Dakota experiment (default is
            'vector_parameter_study').
        variables : str, optional
            Type of variables used in Dakota experiment (default is
            'continuous_design').
        interface : str, optional
            Type of interface used in Dakota experiment (default is
            'direct').
        responses : str, optional
            Type of responses used in Dakota experiment (default is
            'response_functions').
        **kwargs
            Arbitrary keyword arguments.

        Examples
        --------
        Create a generic Dakota experiment:

        >>> x = Experiment()

        Create a vector parameter study experiment:

        >>> x = Experiment(method='vector_parameter_study')

        """
        self.component = component
        if self.component is not None:
            interface = 'fork'
        if method == 'multidim_parameter_study':
            try:
                kwargs['lower_bounds']
            except KeyError:
                kwargs['lower_bounds'] = (-2.0, -2.0)
            try:
                kwargs['upper_bounds']
            except KeyError:
                kwargs['upper_bounds'] = (2.0, 2.0)
        for section in Experiment.blocks:
            cls = self._import(section, eval(section), **kwargs)
            attr = '_' + section
            setattr(self, attr, cls)

    @property
    def environment(self):
        """The environment control block."""
        return self._environment

    @environment.setter
    def environment(self, value):
        """Set the environment control block.

        Parameters
        ----------
        value : obj
            An environment control block object, an instance of a
            subclass of dakotathon.environment.base.EnvironmentBase.

        """
        supr = self._environment.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._environment = value

    @property
    def method(self):
        """The method control block."""
        return self._method

    @method.setter
    def method(self, value):
        """Set the method control block.

        Parameters
        ----------
        value : obj
            A method control block object, an instance of a
            subclass of dakotathon.method.base.MethodBase.

        """
        supr = self._method.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._method = value

    @property
    def variables(self):
        """The variables control block."""
        return self._variables

    @variables.setter
    def variables(self, value):
        """Set the variables control block.

        Parameters
        ----------
        value : obj
            A variables control block object, an instance of a
            subclass of dakotathon.variables.base.VariablesBase.

        """
        supr = self._variables.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._variables = value

    @property
    def interface(self):
        """The interface control block."""
        return self._interface

    @interface.setter
    def interface(self, value):
        """Set the interface control block.

        Parameters
        ----------
        value : obj
            An interface control block object, an instance of a
            subclass of dakotathon.interface.base.InterfaceBase.

        """
        supr = self._interface.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._interface = value

    @property
    def responses(self):
        """The responses control block."""
        return self._responses

    @responses.setter
    def responses(self, value):
        """Set the responses control block.

        Parameters
        ----------
        value : obj
            A responses control block object, an instance of a
            subclass of dakotathon.responses.base.ResponsesBase.

        """
        supr = self._responses.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._responses = value

    def _get_subpackage_namespace(self, subpackage):
        return os.path.splitext(self.__module__)[0] + '.' + subpackage

    def _import(self, subpackage, module, **kwargs):
        namespace = self._get_subpackage_namespace(subpackage) + '.' + module
        module = importlib.import_module(namespace)
        cls = getattr(module, module.classname)
        return cls(**kwargs)

    def __str__(self):
        """The contents of the Dakota input file represented as a string.

        Examples
        --------
        Print the Dakota input file to the console.

        >>> x = Experiment()
        >>> print x
        # Dakota input file
        environment
          tabular_data
            tabular_data_file = 'dakota.dat'
        <BLANKLINE>
        method
          vector_parameter_study
            final_point = 1.1 1.3
            num_steps = 10
        <BLANKLINE>
        variables
          continuous_design = 2
            descriptors = 'x1' 'x2'
            initial_point = -0.3 0.2
        <BLANKLINE>
        interface
          id_interface = 'CSDMS'
          direct
          analysis_driver = 'rosenbrock'
        <BLANKLINE>
        responses
          response_functions = 1
            response_descriptors = 'y1'
          no_gradients
          no_hessians
        <BLANKLINE>
        """
        s = '# Dakota input file\n'
        for section in Experiment.blocks:
            s += str(getattr(self, section))
        return s
