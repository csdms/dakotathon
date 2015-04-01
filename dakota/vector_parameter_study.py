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
            fp.write('# Dakota input file\n')
            fp.write('environment\n')
            fp.write('  tabular_data\n')
            fp.write('    tabular_data_file = {!r}\n'.format(self.data_file))
            fp.write('\n')
            fp.write('method\n')
            fp.write('  {}\n'.format(self.method))
            fp.write('    final_point = ')
            for pt in self.final_point:
                fp.write('{0}{1}'.format(pt, ' '))
            fp.write('\n')
            fp.write('    num_steps = {}\n'.format(self.n_steps))
            fp.write('\n')
            fp.write('variables\n')
            fp.write('  {0}{1}{2}\n'.format(self.variable_type, ' = ',
                                            str(self.n_variables)))
            fp.write('    initial_point = ')
            for pt in self.initial_point:
                fp.write('{0}{1}'.format(pt, ' '))
            fp.write('\n')
            fp.write('    descriptors = ')
            for vd in self.variable_descriptors:
                fp.write('{0!r}{1}'.format(vd, ' '))
            fp.write('\n')
            fp.write('\n')
            fp.write('interface\n')
            fp.write('  {}\n'.format(self.interface))
            fp.write('  analysis_driver = {!r}\n'.format(self.analysis_driver))
            fp.write('  analysis_components = {!r}'.format(self.model))
            for pair in zip(self.response_files, self.response_statistics):
                fp.write(' \'{0[0]}:{0[1]}\''.format(pair))
            fp.write('\n')
            fp.write('  parameters_file = {!r}\n'.format(self.parameters_file))
            fp.write('  results_file = {!r}\n'.format(self.results_file))
            fp.write('  work_directory\n')
            fp.write('    named \'run\'\n')
            fp.write('    directory_tag\n')
            fp.write('    directory_save\n')
            fp.write('  file_save\n')
            fp.write('\n')
            fp.write('responses\n')
            if self.n_response_functions > 0:
                fp.write('  response_functions = {}\n'.format(self.n_response_functions))
            else:
                fp.write('  objective_functions = {}\n'.format(self.n_objective_functions))
            fp.write('    response_descriptors = ')
            for rd in self.response_descriptors:
                fp.write('{0!r}{1}'.format(rd, ' '))
            fp.write('\n')
            fp.write('  no_gradients\n')
            fp.write('  no_hessians\n')
