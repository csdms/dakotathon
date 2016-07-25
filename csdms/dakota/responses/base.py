"""An abstract base class for all Dakota responses."""

from abc import ABCMeta, abstractmethod


class ResponsesBase(object):

    """Describe features common to all Dakota responses."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 responses='response_functions',
                 response_descriptors=(),
                 gradients='no_gradients',
                 hessians='no_hessians',
                 **kwargs):
        """Create a set of default experiment parameters."""
        self.responses = responses
        self._response_descriptors = response_descriptors
        self.gradients = gradients
        self.hessians = hessians

    @property
    def response_descriptors(self):
        """Labels attached to Dakota responses."""
        return self._response_descriptors

    @response_descriptors.setter
    def response_descriptors(self, value):
        """Set labels for Dakota responses.

        Parameters
        ----------
        value : str or list or tuple of str
          The new response labels.

        """
        if type(value) is str:
            value = (value,)
        if not isinstance(value, (tuple, list)):
            raise TypeError("Descriptors must be a string, tuple or list")
        self._response_descriptors = value

    def __str__(self):
        """Define the responses block of a Dakota input file."""
        s = 'responses\n'
        return(s)
