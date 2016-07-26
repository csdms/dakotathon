"""Implementation of a Dakota direct interface."""

from .base import InterfaceBase


classname = 'Direct'


class Direct(InterfaceBase):

    """Define attributes for a Dakota direct interface."""

    def __init__(self, **kwargs):
        """Create a direct interface.

        Parameters
        ----------
        **kwargs
            Optional keyword arguments.

        Examples
        --------
        Create an instance of Direct:

        >>> f = Direct()

        """
        InterfaceBase.__init__(self, **kwargs)
        self.interface = self.__module__.rsplit('.')[-1]

    def __str__(self):
        """Define the block for a direct interface.

        See Also
        --------
        csdms.dakota.interface.base.InterfaceBase.__str__

        """
        s = InterfaceBase.__str__(self)
        s += '\n\n'
        return(s)
