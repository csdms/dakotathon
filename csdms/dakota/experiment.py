"""A template for describing a Dakota experiment."""

import os
import importlib
import inspect


blocks = ['environment', 'method', 'variables', 'interface', 'responses']


class Experiment(object):

    """Describe parameters to create an input file for a Dakota experiment."""

    def __init__(self,
                 method='vector_parameter_study',
                 variables='continuous_design',
                 interface='direct',
                 responses='response_functions',
                 **kwargs):
        """Create a set of default experiment parameters."""
        self.environment = self._import('environment', 'environment', **kwargs)
        self.method = self._import('method', method, **kwargs)
        self.variables = self._import('variables', variables, **kwargs)
        self.interface = self._import('interface', interface, **kwargs)
        self.responses = self._import('responses', responses, **kwargs)

    def _get_subpackage_namespace(self, subpackage):
        return os.path.splitext(self.__module__)[0] + '.' + subpackage

    def _import(self, subpackage, module, **kwargs):
        namespace = self._get_subpackage_namespace(subpackage) + '.' + module
        module = importlib.import_module(namespace)
        cls = getattr(module, module.classname)
        return cls(**kwargs)

    def __str__(self):
        s = '# Dakota input file\n'
        for section in blocks:
            s += str(getattr(self, section))
        return s
