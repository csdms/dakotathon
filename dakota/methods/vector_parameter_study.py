#! /usr/bin/env python
"""Implementation of a Dakota vector parameter study."""

import types
import yaml
from .base import DakotaBase


_classname = 'VectorParameterStudy'

class VectorParameterStudy(DakotaBase):

    """Define parameters for a Dakota vector parameter study."""

    def __init__(self, variable_descriptors=['x1', 'x2'],
                 initial_point=[-0.3, 0.2], final_point=[1.1, 1.3], n_steps=10,
                 response_descriptors=['y1'], **kwargs):
        """Create a new Dakota vector parameter study."""
        DakotaBase.__init__(self, **kwargs)
        self.method = 'vector_parameter_study'
        self.variable_descriptors = variable_descriptors
        self.initial_point = initial_point
        self.final_point = final_point
        self.n_steps = n_steps
        self.response_descriptors = response_descriptors

    @classmethod
    def from_file_like(cls, file_like):
        """Create a VectorParameterStudy instance from a file-like object.

        Parameters
        ----------
        file_like : file_like
            Input parameter file.

        Returns
        -------
        VectorParameterStudy
            A new VectorParameterStudy instance.

        """
        config = {}
        if isinstance(file_like, types.StringTypes):
            with open(file_like, 'r') as fp:
                config = yaml.load(fp.read())
        else:
            config = yaml.load(file_like)
        return cls(**config)

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
                                     len(self.variable_descriptors)) \
            + '    initial_point ='
        for pt in self.initial_point:
            s += ' {}'.format(pt)
        s += '\n' \
             + '    descriptors ='
        for vd in self.variable_descriptors:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
