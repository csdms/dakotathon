"""A class for top-level Dakota settings."""

from .base import EnvironmentBase


classname = "Environment"


class Environment(EnvironmentBase):

    """Describe Dakota environment."""

    def __init__(self, data_file="dakota.dat", **kwargs):
        """Define parameters for the Dakota environment.

        Parameters
        ----------
        data_file : str, optional
            The Dakota tabular data file (default is 'dakota.dat').
        **kwargs
            Optional keyword arguments.

        """
        EnvironmentBase.__init__(self, **kwargs)
        self.data_file = data_file

    def __str__(self):
        """Define the environment block of a Dakota input file."""
        s = EnvironmentBase.__str__(self)
        s += "  tabular_data\n" + "    tabular_data_file = {!r}\n\n".format(
            self.data_file
        )
        return s
