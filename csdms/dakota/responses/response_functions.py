"""Implementation of the Dakota response_function response type."""

from .base import ResponsesBase


classname = 'ResponseFunctions'


class ResponseFunctions(ResponsesBase):

    """Define attributes for Dakota response functions."""

    def __init__(self,
                 response_descriptors=('y1',),
                 response_files=(),
                 response_statistics=('mean',),
                 **kwargs):
        ResponsesBase.__init__(self, **kwargs)
        self.responses = self.__module__.rsplit('.')[-1]
        self._response_descriptors = response_descriptors
        self._response_files = response_files
        self._response_statistics = response_statistics

    @property
    def response_files(self):
        """Model output files used in Dakota responses."""
        return self._response_files

    @response_files.setter
    def response_files(self, value):
        """Set model output files used in Dakota responses.

        Parameters
        ----------
        value : list or tuple of str
          The new response files.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Response files must be a tuple or a list")
        self._response_files = value

    @property
    def response_statistics(self):
        """Model output statistics used in Dakota responses."""
        return self._response_statistics

    @response_statistics.setter
    def response_statistics(self, value):
        """Set model output statistics used in Dakota responses.

        Parameters
        ----------
        value : list or tuple of str
          The new response statistics.

        """
        if not isinstance(value, (tuple, list)):
            raise TypeError("Response statistics must be a tuple or a list")
        self._response_statistics = value

    def __str__(self):
        """Define the responses block of a Dakota input file."""
        n_descriptors = len(self.response_descriptors)
        s = ResponsesBase.__str__(self)
        s += '  response_functions = {}\n'.format(n_descriptors)
        s += '    response_descriptors ='
        for rd in self.response_descriptors:
            s += ' {!r}'.format(rd)
        s += '\n' \
             + '  {}\n'.format(self.gradients) \
             + '  {}\n'.format(self.hessians)
        s += '\n'
        return(s)
