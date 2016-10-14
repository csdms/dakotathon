"""An abstract base class for all Dakota interfaces."""

from abc import ABCMeta, abstractmethod


class InterfaceBase(object):

    """Describe features common to all Dakota interfaces."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 interface='direct',
                 id_interface='CSDMS',
                 analysis_driver='rosenbrock',
                 asynchronous=False,
                 evaluation_concurrency=2,
                 **kwargs):
        """Create a default interface.

        Parameters
        ----------
        interface : str, optional
            The Dakota interface type (default is 'direct').
        id_interface : str, optional
            Interface identifier.
        analysis_driver : str, optional
            Name of analysis driver for Dakota experiment (default is
            'rosenbrock').
        asynchronous : bool, optional
            Set to perform asynchronous evaluations (default is False).
        evaluation_concurrency : int, optional
            Number of concurrent evaluations (default is 2).
        **kwargs
            Optional keyword arguments.

        """
        self.interface = interface
        self.id_interface = id_interface
        self.analysis_driver = analysis_driver
        self._asynchronous = asynchronous
        self._evaluation_concurrency = evaluation_concurrency

    @property
    def asynchronous(self):
        """State of Dakota evaluation concurrency."""
        return self._asynchronous

    @asynchronous.setter
    def asynchronous(self, value):
        """Toggle Dakota evaluation concurrency.

        Parameters
        ----------
        value : bool
          True if evaluation concurrency is enabled.

        """
        if not isinstance(value, bool):
            raise TypeError("Asynchronous must be a bool")
        self._asynchronous = value

    @property
    def evaluation_concurrency(self):
        """Number of concurrent evaluations."""
        return self._evaluation_concurrency

    @evaluation_concurrency.setter
    def evaluation_concurrency(self, value):
        """Set the number of concurrent evaluations.

        Parameters
        ----------
        value : int
          The number of concurrent evaluations.

        """
        if not isinstance(value, int):
            raise TypeError("Evaluation concurrency must be a int")
        self._evaluation_concurrency = value

    def __str__(self):
        """Define the interface block of a Dakota input file."""
        s = 'interface\n' \
            + '  id_interface = {!r}\n'.format(self.id_interface) \
            + '  {}\n'.format(self.interface) \
            + '  analysis_driver = {!r}'.format(self.analysis_driver)
        if self.asynchronous:
            s += '\n' \
                 + '  asynchronous'
            s += '\n' \
                 + '  evaluation_concurrency =' \
                 + ' {}'.format(self.evaluation_concurrency)
        return(s)
