"""An abstract base class for all Dakota variable types."""

from abc import ABCMeta, abstractmethod


class VariableBase(object):

    """Describe features common to all Dakota variable types."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 variables='continuous_design',
                 descriptors=(),
                 **kwargs):
        """Create a set of default experiment parameters."""
        self.variables = variables
        self._descriptors = descriptors

    @property
    def descriptors(self):
        """Labels attached to Dakota variables."""
        return self._descriptors

    @descriptors.setter
    def descriptors(self, value):
        """Set labels for Dakota variables.

        Parameters
        ----------
        value : str or list or tuple of str
          The new variables labels.

        """
        if type(value) is str:
            value = (value,)
        if not isinstance(value, (tuple, list)):
            raise TypeError("Descriptors must be a string, tuple or list")
        self._descriptors = value

    @abstractmethod
    def variables_block(self):
        """Define the variables block of a Dakota input file."""
        s = 'variables\n' \
            + ' {0} = {1}\n'.format(self.variables,
                                    len(self.descriptors))
        s += '    descriptors ='
        for vd in self.descriptors:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
