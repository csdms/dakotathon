#!/usr/bin/env python
"""Basic Model Interface for the Dakota iterative systems analysis toolkit."""

from basic_modeling_interface import Bmi
from .dakota import Dakota


class BmiDakota(Bmi):

    """The BMI implementation for the CSDMS Dakota interface."""

    _name = 'Dakota'

    def __init__(self):
        """Create a BmiDakota instance."""
        self._model = None
        self._time = 0.0

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
        self._time += self.get_time_step()

    def finalize(self):
        """Remove the Dakota instance."""
        self._model = None

    def get_component_name(self):
        """Name of the component."""
        return self._name

    def get_start_time(self):
        """Start time of model."""
        return 0.0

    def get_end_time(self):
        """End time of model."""
        return 1.0

    def get_current_time(self):
        """Current time of model."""
        return self._time

    def get_time_step(self):
        """Time step of model."""
        return 1.0


class CenteredParameterStudy(BmiDakota):

    """BMI implementation of a Dakota centered parameter study."""

    _name = 'CenteredParameterStudy'

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method='centered_parameter_study')
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class MultidimParameterStudy(BmiDakota):

    """BMI implementation of a Dakota multidim parameter study."""

    _name = 'MultidimParameterStudy'

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method='multidim_parameter_study')
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class VectorParameterStudy(BmiDakota):

    """BMI implementation of a Dakota vector parameter study."""

    _name = 'VectorParameterStudy'

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method='vector_parameter_study')
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class Sampling (BmiDakota):

    """BMI implementation of a Dakota sampling study."""

    _name = 'Sampling'

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method='sampling',
                                 variables='uniform_uncertain')
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()
