"""A template for describing a Dakota experiment."""

import os
import importlib


class Experiment(object):

    """Describe parameters to create an input file for a Dakota experiment."""

    def __init__(self,
                 environment='environment',
                 method='vector_parameter_study',
                 variables='continuous_design',
                 interface='direct',
                 responses='response_functions',
                 **kwargs):
        """Create a set of default experiment parameters."""
        self._blocks = ('environment', 'method', 'variables',
                        'interface', 'responses')
        for section in self._blocks:
            cls = self._import(section, eval(section), **kwargs)
            attr = '_' + section
            setattr(self, attr, cls)

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        supr = self._environment.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._environment = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        supr = self._method.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._method = value

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        supr = self._variables.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._variables = value

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, value):
        supr = self._interface.__class__.__bases__[0]
        if not isinstance(value, supr):
            raise TypeError("Must be a subclass of " + str(supr))
        self._interface = value

    @property
    def responses(self):
        return self._responses

    @responses.setter
    def responses(self, value):
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
        s = '# Dakota input file\n'
        for section in self._blocks:
            s += str(getattr(self, section))
        return s
