#! /usr/bin/env python
"""Implementation of a Dakota vector parameter study."""

from .dakota import Dakota


class VectorParameterStudy(Dakota):
    """Set up a Dakota vector parameter study."""

    def __init__(self):
        """Create a new Dakota vector parameter study."""
        Dakota.__init__(self)
        self.method = 'vector_parameter_study'
        self.initial_point = []
        self.final_point = []
        self.n_steps = 0

    def write(self):
        """Write a Dakota input file."""
        indent = '  '
        with open(self.input_file, 'w') as fp:
            fp.write('# Dakota input file\n')
            fp.write('environment\n')
            fp.write('{0}{1}\n'.format(indent, 'tabular_data'))
            fp.write('{0}{0}{1} = {2!r}\n'.format(indent,
                                                  'tabular_data_file',
                                                  self.data_file))
            fp.write('\nmethod\n')
            fp.write('{0}{1}\n'.format(indent, self.method))
