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

