#! /usr/bin/env python
"""Helper functions for processing Dakota parameter and results files."""

import os
import subprocess
import re
import yaml
import numpy as np
import collections


def is_dakota_installed():
    """Check whether Dakota is installed and in the execution path.

    Returns
    -------
    bool
      True if Dakota is callable.

    """
    try:
        subprocess.check_call(['dakota', '--version'])
    except (subprocess.CalledProcessError, OSError):
        return False
    else:
        return True


def which(prog, env=None):
    """Call the OS `which` function.

    Parameters
    ----------
    prog : str
      The command name.
    env : str, optional
      An environment variable.

    Returns
    -------
    The path to the command, or None if the command is not found.

    """
    prog = os.environ.get(env or prog.upper(), prog)

    try:
        prog = subprocess.check_output(['/usr/bin/which', prog],
                                       stderr=open('/dev/null', 'w')).strip()
    except subprocess.CalledProcessError:
        return None
    else:
        return prog


def which_dakota():
    """Locate the Dakota executable.

    Returns
    -------
    The path to the Dakota executable, or None if Dakota is not found.

    """
    return which('dakota')


def add_dyld_library_path():
    """Add the `DYLD_LIBRARY_PATH` environment variable for Dakota."""
    try:
        dakota_exe = which_dakota()
        dakota_dir = os.path.dirname(os.path.dirname(dakota_exe))
        os.environ['DYLD_LIBRARY_PATH'] = os.path.join(dakota_dir, 'bin') \
                                          + os.path.pathsep \
                                          + os.path.join(dakota_dir, 'lib')
    except AttributeError:
        return None


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


def get_attributes(obj):
    """Get and format the attributes of an object.

    Parameters
    ----------
    section
      An object that has attributes.

    Returns
    -------
    dict
      The object's attributes.

    """
    attrs = obj.__dict__.copy()
    for key in attrs:
        if key.startswith('_'):
            new_key = key.lstrip('_')
            attrs[new_key] = attrs.pop(key)
    return attrs


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


def deserialize(config_file):
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
    arr_values = np.asarray(values)
    arr_labels = np.asarray(labels)
    results = np.column_stack((arr_values, arr_labels))
    np.savetxt(results_file, results, delimiter="\t", fmt='%s')


def to_iterable(x):
    """Get an iterable version of an input.

    Parameters
    ----------
    x
      Anything.

    Returns
    -------
    If the input isn't iterable, or is a string, then a tuple; else,
    the input.

    Notes
    -----
    Courtesy http://stackoverflow.com/a/6711233/1563298

    """
    if isinstance(x, collections.Iterable) and not isinstance(x, basestring):
        return x
    else:
        return (x,)


def configure_parameters(params):
    """Preprocess Dakota parameters prior to committing to a config file.

    Parameters
    ----------
    params : dict
      Configuration parameters for a Dakota experiment that map to the
      items in the Dakota configuration file, **dakota.yaml**.

    Returns
    -------
    (dict, dict)
      An updated dict of Dakota configuration parameters, and a dict
      of substitutions used to create the Dakota template ("dtmpl")
      file.

    """
    try:
        params['component']
    except KeyError:
        try:
            params['plugin']
        except KeyError:
            params['component'] = params['plugin'] = ''
        else:
            params['analysis_driver'] = 'dakota_run_plugin'
            params['component'] = ''
    else:
        params['analysis_driver'] = 'dakota_run_component'
        params['plugin'] = ''

    to_check = ['descriptors',
                'response_descriptors',
                'response_statistics']
    for item in to_check:
        if isinstance(params[item], basestring):
            params[item] = [params[item]]

    subs = {}
    for item in params['descriptors']:
        subs[item] = '{' + item + '}'

    return params, subs
