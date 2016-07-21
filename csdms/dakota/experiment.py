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
            setattr(self, section, cls)

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
