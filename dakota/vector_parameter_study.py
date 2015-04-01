#! /usr/bin/env python
"""Implementation of a Dakota vector parameter study."""

from .dakota import Dakota


class VectorParameterStudy(Dakota):
    """Set up a Dakota vector parameter study."""

    def __init__(self, input_file='dakota.in'):
        """Create a new Dakota vector parameter study."""
        Dakota.__init__(self, input_file)
        self.method = 'vector_parameter_study'
        self.initial_point = [-0.3, 0.2]
        self.final_point = [1.1, 1.3]
        self.n_steps = 10
        self.interface = 'direct'
        self.analysis_driver = 'rosenbrock'

    def method_block(self):
        """Define the method block of a Dakota input file."""
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    final_point ='
        for pt in self.final_point:
            s += ' {}'.format(pt)
        s += ('\n' \
            + '    num_steps = {}\n\n'.format(self.n_steps))
        return(s)

    def variables_block(self):
        """Define the variables block of a Dakota input file."""
        s = 'variables\n' \
            + '  {0} = {1}\n'.format(self.variable_type, self.n_variables) \
            + '    initial_point ='
        for pt in self.initial_point:
            s += ' {}'.format(pt)
        s += '\n' \
             + '    descriptors ='
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
        s += '  parameters_file = {!r}\n'.format(self.parameters_file) \
             + '  results_file = {!r}\n'.format(self.results_file) \
             + '  work_directory\n' \
             + '    named \'run\'\n' \
             + '    directory_tag\n' \
             + '    directory_save\n' \
             + '  file_save\n\n'
        return(s)
