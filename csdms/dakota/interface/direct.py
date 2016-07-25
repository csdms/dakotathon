"""Implementation of a Dakota direct interface."""

from .base import InterfaceBase


classname = 'Direct'


class Direct(InterfaceBase):

    """Define attributes for a Dakota direct interface."""

    def __init__(self, **kwargs):
        InterfaceBase.__init__(self, **kwargs)
        self.interface = self.__module__.rsplit('.')[-1]

    def __str__(self):
        """Define the block for a direct interface."""
        s = InterfaceBase.__str__(self)
        s += '\n\n'
        return(s)
