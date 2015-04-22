#!/usr/bin/env python
"""Basic Model Interface for the Dakota iterative systems analysis toolkit."""

from .core import Dakota


class BmiDakota(object):

    """Perform a Dakota experiment on a component."""

    _name = 'Dakota'

    def __init__(self):
        """Create a BmiDakota instance."""
        self._model = None

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota()
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()

    def update(self):
        """Run Dakota."""
        self._model.run()

    def finalize(self):
        """Remove the Dakota instance."""
        self._model = None

    def get_component_name(self):
        """Name of the component."""
        return self._name
