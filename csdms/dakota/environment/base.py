"""An abstract base class for top-level Dakota settings."""

from abc import ABCMeta, abstractmethod


class EnvironmentBase(object):

    """Describe features common to all Dakota environments."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    def __str__(self):
        """The header for the environment block of a Dakota input file."""
        s = 'environment\n'
        return(s)
