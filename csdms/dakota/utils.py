#! /usr/bin/env python
"""Helper functions for processing Dakota parameter and results files."""

import subprocess
import re
import yaml


def is_dakota_installed():
    """Check whether Dakota is installed and in the execution path.

    Returns
    -------
    bool
      True if Dakota is callable.

    """
    try:
        subprocess.check_call(['dakota', '--version'])
    except subprocess.CalledProcessError:
        return False
    else:
        return True

def get_response_descriptors(params_file):
    """Extract response descriptors from a Dakota parameters file.

    Parameters
    ----------
    params_file : str
      The path to a Dakota parameters file.

    Returns
    -------
    list
      A list of response descriptors for the Dakota experiment.

    """
    labels = []
    try:
        with open(params_file, 'r') as fp:
            for line in fp:
                if re.search('ASV_', line):
                    labels.append(''.join(re.findall(':(\S+)', line)))
    except IOError:
        return None
    else:
        return labels


def get_configuration_file(params_file):
    """Extract the configuration filepath from a Dakota parameters file.

    Parameters
    ----------
    params_file : str
      The path to a Dakota parameters file.

    Returns
    -------
    str
      The path to the configuration file for the Dakota experiment.

    """
    with open(params_file, 'r') as fp:
        for line in fp:
            if re.search('AC_1', line):
                return line.split('AC_1')[0].strip()


def get_configuration(config_file):
    """Load settings from a YAML configuration file.

    Returns
    -------
    dict
      Configuration settings in a dict.

    """
    with open(config_file, 'r') as fp:
        return yaml.load(fp)


def compute_statistic(statistic, array):
    """Compute the statistic used in a Dakota response function.

    Parameters
    ----------
    statistic : str
      A string with the name of the statistic to compute ('mean',
      'median', etc.).
    array : array_like
      An array data structure, such as a numpy array.

    Returns
    -------
    float
      The value of the computed statistic.

    """
    import numpy as np
    return np.__getattribute__(statistic)(array)


def write_results(results_file, values, labels):
    """Write a Dakota results file from a set of input values.

    Parameters
    ----------
    results_file : str
      The path to a Dakota results file.
    values : array_like
      A list or array of numeric values.
    labels : str
      A list of labels to attach to the values.

    """
    with open(results_file, 'w') as fp:
        for i in range(len(values)):
            fp.write('{0}\t{1}\n'.format(values[i], labels[i]))
