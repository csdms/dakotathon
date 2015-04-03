#! /usr/bin/env python
"""A base class for all Dakota experiments."""

from abc import ABCMeta, abstractmethod


class DakotaBase(object):
    """Describe features common to all Dakota experiments."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """Create a set of default experiment parameters."""
        self.model = None
        self.data_file = 'dakota.dat'

        self.method = None

        self.variable_type = 'continuous_design'
        self.n_variables = 0
        self.variable_descriptors = []

        self.interface = 'direct'
        self.analysis_driver = 'rosenbrock'
        self.parameters_file = 'params.in'
        self.results_file = 'results.out'

        self.n_responses = 0
        self.is_objective_function = False
        self.response_descriptors = []
        self.response_files = []
        self.response_statistics = []

    def environment_block(self):
        """Define the environment block of a Dakota input file."""
        s = '# Dakota input file\n' \
            + 'environment\n' \
            + '  tabular_data\n' \
            + '    tabular_data_file = {!r}\n\n'.format(self.data_file)
        return(s)

    def method_block(self):
        """Define the method block of a Dakota input file."""
        s = 'method\n' \
            + '  {}\n\n'.format(self.method)
        return(s)

    def variables_block(self):
        """Define the variables block of a Dakota input file."""
        s = 'variables\n' \
            + '  {0} = {1}\n'.format(self.variable_type, self.n_variables)
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
        if self.model is not None:
            s += '  analysis_components = {!r}'.format(self.model)
            for pair in zip(self.response_files, self.response_statistics):
                s += ' \'{0[0]}:{0[1]}\''.format(pair)
            s += '\n'
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
        s = 'responses\n'
        if self.is_objective_function:
            s += '  objective_functions = {}\n'.format(self.n_responses)
        else:
            s += '  response_functions = {}\n'.format(self.n_responses)
        s += '    response_descriptors ='
        for rd in self.response_descriptors:
            s += ' {!r}'.format(rd)
        s += '\n' \
             + '  no_gradients\n' \
             + '  no_hessians\n'
        return(s)

    def autogenerate_descriptors(self):
        """Quickly make generic variable and response descriptors."""
        self.variable_descriptors = ['x' + str(i+1) for i in
                                     range(self.n_variables)]
        self.response_descriptors = ['y' + str(i+1) for i in
                                     range(self.n_responses)]
