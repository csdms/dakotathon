"""Implementation of a Dakota fork interface."""

import os
from .base import InterfaceBase


classname = "Fork"


class Fork(InterfaceBase):

    """Define attributes for a Dakota fork interface."""

    def __init__(self, **kwargs):
        """Create a fork interface.

        Parameters
        ----------
        **kwargs
            Optional keyword arguments.

        Examples
        --------
        Create an instance of Fork:

        >>> f = Fork()

        """
        InterfaceBase.__init__(self, **kwargs)
        self.interface = self.__module__.rsplit(".")[-1]
        try:
            self._configuration_file = os.path.abspath(
                os.path.join(
                    kwargs.pop("run_directory"), kwargs.pop("configuration_file")
                )
            )
        except KeyError:
            self._configuration_file = os.path.abspath("dakota.yaml")

    def __str__(self):
        """Define the block for a fork interface.

        See Also
        --------
        dakotathon.interface.base.InterfaceBase.__str__

        """
        s = InterfaceBase.__str__(self)
        s += "\n" + "  analysis_components = {!r}\n".format(self._configuration_file)
        s += (
            "  parameters_file = {!r}\n".format(self.parameters_file)
            + "  results_file = {!r}\n".format(self.results_file)
            + "  work_directory\n"
            + "    named {!r}\n".format(self.work_directory)
            + "    directory_tag\n"
            + "    directory_save\n"
            + "  file_save\n"
        )
        s += "\n"
        return s
