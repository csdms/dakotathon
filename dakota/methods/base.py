#! /usr/bin/env python
"""An abstract base class for all Dakota experiments."""

from abc import ABCMeta, abstractmethod


class DakotaBase(object):

    """Describe features common to all Dakota experiments."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, component=None, template_file=None,
                 method=None, configuration_file='config.yaml',
                 run_directory='.', input_files=[],
                 data_file='dakota.dat',
                 variable_type='continuous_design',
                 variable_descriptors=[], interface='direct',
                 analysis_driver='rosenbrock',
                 is_objective_function=False, response_descriptors=[],
                 response_files=[], response_statistics=[], **kwargs):
        """Create a set of default experiment parameters."""
        self.component = component
        self.configuration_file = configuration_file
        self.run_directory = run_directory
        self.template_file = template_file
        self.input_files = input_files
        self.data_file = data_file
        self.method = method
        self.variable_type = variable_type
        self.variable_descriptors = variable_descriptors
        self.interface = interface
        self.analysis_driver = analysis_driver
        self.parameters_file = 'params.in'
        self.results_file = 'results.out'
        self.is_objective_function = is_objective_function
        self.response_descriptors = response_descriptors
        self.response_files = response_files
        self.response_statistics = response_statistics

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
                                    len(self.variable_descriptors))
        s += '    descriptors ='
        for vd in self.variable_descriptors:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)

    def interface_block(self):
        """Define the interface block of a Dakota input file."""
        s = 'interface\n' \
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
