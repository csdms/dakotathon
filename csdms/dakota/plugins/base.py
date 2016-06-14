#! /usr/bin/env python
"""An abstract base class for all Dakota component plugins."""

from abc import ABCMeta, abstractmethod


def write_tmpl_file(base_tmpl_file, base_input_file, parameter_names):
    """Create a template HydroTrend input file used by Dakota.

    The tmpl file is a HydroTrend input file, but with the
    parameters used by Dakota replaced with their descriptors set
    in the Dakota input file. The tmpl file is written to the
    current directory.

    Parameters
    ----------
    base_tmpl_file : str
      The path to the template file defined for the HydroTrend
      component.
    base_input_file : str
      A HydroTrend input file that contains parameter values for a
      HydroTrend simulation.
    parameter_names : list of str
      A list of HydroTrend parameter names (standard names) that
      will be evaluated by Dakota.

    Returns
    -------
    str or None
      The path to the new tmpl file, or None on an error.

    """
    import re

    with open(base_tmpl_file, 'r') as fp:
        txt_base_tmpl = fp.read().split('\n')
    with open(base_input_file, 'r') as fp:
        txt_base_input = fp.read().split('\n')

    if len(txt_base_tmpl) != len(txt_base_input):
        raise

    for p_name in parameter_names:
        for i, line_tmpl in enumerate(txt_base_tmpl):
            if re.search(p_name, line_tmpl):
                line_input = txt_base_input[i]
                line_tmpl_split = line_tmpl.strip().split()
                line_input_split = line_input.strip().split()
                for j, item in enumerate(line_tmpl_split):
                    if item.startswith('{' + p_name):
                        line_input_split[j] = '{' + p_name + '}'
                txt_base_input[i] = ' '.join(line_input_split)

    tmpl_file = 'HYDRO.IN.tmpl'
    with open(tmpl_file, 'w') as fp:
        fp.write('\n'.join(txt_base_input))
        return tmpl_file


class PluginBase(object):

    """Describe features common to all Dakota plugins."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        """Define default attributes."""
        pass

    @abstractmethod
    def setup(self, config):
        """Configure component inputs.

        Sets attributes using information from the run configuration
        file. The Dakota parsing utility ``dprepro`` reads parameters
        from Dakota to create a new input file from a template.

        Parameters
        ----------
        config : dict
          Stores configuration settings for a Dakota experiment.

        """
        pass

    @abstractmethod
    def call(self):
        """Call the component through the shell."""
        pass

    @abstractmethod
    def load(self, output_file):
        """Read data from a component output file.

        Parameters
        ----------
        output_file : str
          The path to a component output file.

        Returns
        -------
        array_like
          A numpy array, or None on an error.

        """
        pass

    @abstractmethod
    def calculate(self):
        """Calculate Dakota response functions."""
        pass

    @abstractmethod
    def write(self, params_file, results_file):
        """Write a Dakota results file.

        Parameters
        ----------
        params_file : str
          A Dakota parameters file.
        results_file : str
          A Dakota results file.

        """
        pass
