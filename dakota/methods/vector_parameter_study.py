#! /usr/bin/env python
"""Implementation of a Dakota vector parameter study."""

from .base import DakotaBase


def method():
    """Call this helper function to create a VectorParameterStudy object.

    Every subclass of DakotaBase implements a **method** function to
    return an instance of the class stored in the module. This way,
    only the module name (which matches the Dakota ``method`` keyword)
    is needed to create an instance of the subclass.

    Returns
    -------
    object
      An instance of VectorParameterStudy.

    Examples
    --------
    Call this function instead of the class constructor to obtain a
    VectorParameterStudy instance:

    >>> v = method() # instead of v = VectorParameterStudy()

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
        self.interface = 'direct'
        self.analysis_driver = 'rosenbrock'
        self.generate_descriptors()

    def method_block(self):
        """Define a vector parameter study method block for a Dakota input file.

        See Also
        --------
        dakota.methods.base.DakotaBase.method_block

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
        """Define a vector parameter study variables block for a Dakota input file.

        See Also
        --------
        dakota.methods.base.DakotaBase.variables_block

        """
        s = 'variables\n' \
            + '  {0} = {1}\n'.format(self.variable_type, 
                                     len(self.variable_descriptors) \
            + '    initial_point ='
        for pt in self.initial_point:
            s += ' {}'.format(pt)
        s += '\n' \
             + '    descriptors ='
        for vd in self.variable_descriptors:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
