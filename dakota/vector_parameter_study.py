#! /usr/bin/env python
"""Implementation of a Dakota vector parameter study."""

from .dakota import Dakota


class VectorParameterStudy(Dakota):
    """Set up a Dakota vector parameter study."""

    def __init__(self):
        """Create a new Dakota vector parameter study."""
        Dakota.__init__(self)
        self.method = 'vector_parameter_study'
        self.initial_point = [-0.3, 0.2]
        self.final_point = [1.1, 1.3]
        self.n_steps = 10
        self.interface = 'direct'
        self.analysis_driver = 'rosenbrock'

    def write(self):
        """Write a Dakota input file."""
        with open(self.input_file, 'w') as fp:
            fp.write(self.environment_block())
            fp.write(self.method_block())
            fp.write(self.variables_block())
            fp.write(self.interface_block())
            fp.write(self.responses_block())

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
