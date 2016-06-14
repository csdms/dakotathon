#! /usr/bin/env python
"""An abstract base class for all Dakota component plugins."""

import os
import re
import yaml
from abc import ABCMeta, abstractmethod


def write_dflt_file(tmpl_file, parameters_file):
    """Create a component input file populated with default values.

    Parameters
    ----------
    tmpl_file : str
      The path to the CSDMS template file defined for the component.
    parameters_file : str
      The path to the CSDMS parameters file defined for the component.

    Returns
    -------
    str or None
      The path to the new dflt file, or None on an error.

    """
    with open(tmpl_file, 'r') as fp:
        template = fp.read().split('\n')

    with open(parameters_file, 'r') as fp:
        parameters = yaml.safe_load(fp)

    parameters['_run_duration'] = {'value': {'default': '1'}}

    defaults = template
    for p_name in parameters.keys():
        p_default = str(parameters[p_name]['value']['default'])
        for i, line_tmpl in enumerate(template):
            if re.search(p_name, line_tmpl):
                line_dflt_split = defaults[i].strip().split()
                for j, item in enumerate(line_tmpl.strip().split()):
                    if item.startswith('{' + p_name):
                        line_dflt_split[j] = p_default
                defaults[i] = ' '.join(line_dflt_split)

    dflt_file = os.path.splitext(tmpl_file)[0] + '.dflt'
    with open(dflt_file, 'w') as ofp:
        ofp.write('\n'.join(defaults))

    return dflt_file


def write_dtmpl_file(tmpl_file, dflt_input_file, parameter_names):
    """Create a template input file for use by Dakota.

    In the CSDMS framework, the tmpl file is an input file for a
    component, but with the parameter values replaced by
    `{parameter_name}`. Dakota uses the same idea. This function
    creates a Dakota dtmpl file from a CSDMS component tmpl file. Only
    the parameters used by Dakota are left in the tmpl format; the
    remainder are populated with default values for the component. The
    dtmpl file is written to the current directory.

    Parameters
    ----------
    tmpl_file : str
      The path to the CSDMS template file defined for the component.
    dflt_input_file : str
      An input file that contains the default parameter values for a
      component.
    parameter_names : list of str
      A list of parameter names for the component to be evaluated by
      Dakota.

    Returns
    -------
    str or None
      The path to the new dtmpl file, or None on an error.

    """
    with open(tmpl_file, 'r') as fp:
        txt_base_tmpl = fp.read().split('\n')
    with open(dflt_input_file, 'r') as fp:
        txt_dflt_input = fp.read().split('\n')

    for p_name in parameter_names:
        for i, line_tmpl in enumerate(txt_base_tmpl):
            if re.search(p_name, line_tmpl):
                line_input_split = txt_dflt_input[i].strip().split()
                for j, item in enumerate(line_tmpl.strip().split()):
                    if item.startswith('{' + p_name):
                        line_input_split[j] = '{' + p_name + '}'
                txt_dflt_input[i] = ' '.join(line_input_split)

    dtmpl_file = os.path.splitext(tmpl_file)[0] + '.dtmpl'
    with open(dtmpl_file, 'w') as fp:
        fp.write('\n'.join(txt_dflt_input))

    return dtmpl_file


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
