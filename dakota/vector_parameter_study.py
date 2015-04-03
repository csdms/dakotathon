#! /usr/bin/env python
"""Implementation of a Dakota vector parameter study."""

from .dakota_base import DakotaBase


def method():
    """A helper function to return a VectorParameterStudy object.

    Returns
    -------
    object
      An instance of VectorParameterStudy.

    Examples
    --------
    Call this function instead of the class constructor to obtain a
    VectorParameterStudy instance.

    >>> import dakota.vector_parameter_study as m
    >>> v = m.method() # instead of v = m.VectorParameterStudy()
    """
    return VectorParameterStudy()

class VectorParameterStudy(DakotaBase):
    """Define parameters for a Dakota vector parameter study."""

    def __init__(self):
        """Create a new Dakota vector parameter study."""
        DakotaBase.__init__(self)
        self.method = 'vector_parameter_study'
        self.initial_point = [-0.3, 0.2]
        self.final_point = [1.1, 1.3]
        self.n_steps = 10
        self.n_variables = len(self.initial_point)
        self.interface = 'direct'
        self.analysis_driver = 'rosenbrock'
        self.n_responses = 1
        self.autogenerate_descriptors()

    def method_block(self):
        """Define the method block of a Dakota input file for a vector
        parameter study.
        """
        s = 'method\n' \
            + '  {}\n'.format(self.method) \
            + '    final_point ='
        for pt in self.final_point:
            s += ' {}'.format(pt)
        s += ('\n' \
            + '    num_steps = {}\n\n'.format(self.n_steps))
        return(s)

    def variables_block(self):
        """Define the variables block of a Dakota input file for a vector
        parameter study.
        """
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
