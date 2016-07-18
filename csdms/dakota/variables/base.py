"""An abstract base class for all Dakota variable types."""

from abc import ABCMeta, abstractmethod


class VariableBase(object):

    """Describe features common to all Dakota variable types."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 variable_type='continuous_design',
                 variables=(),
                 **kwargs):
        """Create a set of default experiment parameters."""
        self.variable_type = variable_type
        self._variables = variables

    @property
    def variables(self):
        """Labels attached to Dakota variables."""
        return self._variables

    @variables.setter
    def variables(self, value):
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
        self._variables = value

    @abstractmethod
    def variables_block(self):
        """Define the variables block of a Dakota input file."""
        s = 'variables\n' \
            + ' {0} = {1}\n'.format(self.variable_type,
                                    len(self.variables))
        s += '    descriptors ='
        for vd in self.variables:
            s += ' {!r}'.format(vd)
        s += '\n\n'
        return(s)
