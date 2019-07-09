#! /usr/bin/env python
"""Implementation of a Dakota PSUADE MOAT study.

Description from the Dakota Reference Guide: 
https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-psuade_moat.html

"The Morris One-At-A-Time (MOAT) method, originally proposed by Morris 
[1991], is a screening method, designed to explore a computational 
model to distinguish between input variables that have negligible, 
linear and additive, or nonlinear or interaction effects on the output. 
The computer experiments performed consist of individually randomized 
designs which vary one input factor at a time to create a sample of its 
elementary effects.
    
"The number of samples (samples) must be a positive integer multiple of 
(number of continuous design variable + 1) 
and will be automatically adjusted if misspecified

"The number of partitions (partitions) applies to each variable being 
studied and must be odd 
(the number of MOAT levels per variable is partitions + 1). 
This will also be adjusted at runtime as necessary.

For information on practical use of this method, see Saltelli, et al.,
[2004]."

The literature listed below recommends that the sample size should be 
4 to 10 times the value (number of continuous design variable + 1) 
such that 4 to 10 individually randomized experiments to calculate 
elementary effects are acomplished. Each of these elementary effects
experiments represent a trajectory through parameter space starting at
a randomly chosen point on the lattice created by discretizing 
parameter space using the number of partitions specified. From the 
inital point, the model is evaluated (number of continuous design 
variable + 1) times, creating a trajectory through parameter space and
(number of continuous design variable) elementary effects. 
The model is not evaluated at the randomly chosen start point. 

There is little guidance regarding the number of partitions. 

Note that each trajectory must be independent and that intial start 
locations are all randomly chosen at the onset of the study. If a new
trajectory has overlapping points with a prior trajectory, this new 
trajectory will not be used. Thus, the final number of points evaluated
may be less than the number of samples desired by a multiple of 
(number of continuous design variable + 1) 

M. D. Morris. Factorial sampling plans for preliminary computational 
experiments. Technometrics, 33(2):161-174, 1991.

A. Saltelli, S. Tarantola, F. Campolongo, and M. Ratto. Sensitivity 
Analysis in Practice: A Guide to Assessing Scientific Models.
John Wiley & Sons, 2004.

Katherine Barnhart
(barnhark@colorado.edu)
March 2017
"""

from .base import MethodBase

classname = "PsuadeMoat"


class PsuadeMoat(MethodBase):

    """Define parameters for a Dakota PSUADE MOAT study."""

    def __init__(
        self, samples=12, seed=500, partitions=5, model_pointer=None, **kwargs
    ):
        """Create a new Dakota PSUADE MOAT study.
        
        Parameters
        ----------
        samples : array_like of float, optional
          Number of samples (default is 10).
        seed : int, optional
          Random seed (default is 500).
        partitions : array_like of int, optional
          Number of partitions (default = 5)
        model_pointer : str, optional
          The id_model of the model block used for the analysis. This should be
          specified if multiple models are being used. If none is specified
          Dakota will use the last model block parsed.
          
        Examples
        --------
        Create a default centered parameter study experiment:

        >>> p = PsuadeMoat()

        """
        MethodBase.__init__(self, **kwargs)
        self.method = self.__module__.rsplit(".")[-1]
        self._partitions = partitions
        self._model_pointer = model_pointer

        # samples must be r*(num_parameters+1) enforce this here

        self._samples = samples
        self._seed = seed

    @property
    def model_pointer(self):
        """Model pointer name."""
        return self._model_pointer

    @model_pointer.setter
    def model_pointer(self, value):
        """Set model_pointer name.

        Parameters
        ----------
        value : str
          The new model pointer name

        """
        if not isinstance(value, str):
            raise TypeError("Model pointer name must be str")
        self._model_pointer = value

    @property
    def partitions(self):
        """Number partitions of each parameter dimension."""
        return self._partitions

    @partitions.setter
    def partitions(self, value):
        """Set value of partitions.

        Parameters
        ----------
        value : int
          The partitions value.

        """
        if not isinstance(value, int):
            raise TypeError("Partitions value must be int")
        self._partitions = value

    @property
    def samples(self):
        """Number of samples."""
        return self._samples

    @samples.setter
    def samples(self, value):
        """Set value of samples.

        Parameters
        ----------
        value : int
          The samples value.

        """
        if not isinstance(value, int):
            raise TypeError("Samples value must be int")
        self._samples = value

    @property
    def seed(self):
        """Seed value."""
        return self._seed

    @seed.setter
    def seed(self, value):
        """Set value of seed.

        Parameters
        ----------
        value : int
          The seed value.

        """
        if not isinstance(value, int):
            raise TypeError("Seed value must be int")
        self._seed = value

    def __str__(self):
        """Define a PSUADE MOAT method block.

        See Also
        --------
        dakotathon.method.base.MethodBase.__str__

        """
        s = MethodBase.__str__(self)
        if self._model_pointer is None:
            pass
        else:
            s += "    model_pointer = {} \n".format(self._model_pointer)
        s += "    partitions = {} \n".format(self.partitions)
        s += "    samples = {} \n".format(self.samples)
        s += "    seed = {} \n".format(self.seed)
        s += "\n"
        return s
