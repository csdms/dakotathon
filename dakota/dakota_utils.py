#! /usr/bin/env python
"""Helper functions for processing Dakota parameter and results files."""

import subprocess
import re


def is_dakota_installed():
    """Check whether Dakota is installed and in the execution path.
    
    Returns
    -------
    bool
      True if Dakota is callable.

    """
    try:
        subprocess.call(['dakota', '--version'])
    except OSError:
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
        return(labels)

def get_analysis_components(params_file):
    """Extract the analysis components from a Dakota parameters file.

    The analysis components are returned as a list. First is the name
    of the model being run by Dakota, followed by dicts containing an
    output file to analyze and the statistic to apply to the file.

    Parameters
    ----------
    params_file : str
      The path to a Dakota parameters file.

    Returns
    -------
    list
      A list of analysis components for the Dakota experiment.

    Examples
    --------
    Extract the analysis components from a Dakota parameters file:

    >>> ac = get_analysis_components(params_file)
    >>> ac.pop(0)
    'hydrotrend'
    >>> ac.pop(0)
    {'file': 'HYDROASCII.QS', 'statistic': 'median'}

    Notes
    -----
    The syntax expected by this function is defined in the Dakota
    input file; e.g., for the example cited above, the 'interface'
    section of the input file contains the line:

      analysis_components = 'hydrotrend' 'HYDROASCII.QS:median'

    """
    ac = []
    try:
        with open(params_file, 'r') as fp:
            for line in fp:
                if re.search('AC_1', line):
                    ac.append(line.split('AC_1')[0].strip())
                elif re.search('AC_', line):
                    parts = re.split(':', re.split('AC_', line)[0])
                    ac.append({'file':parts[0].strip(),
                               'statistic':parts[1].strip()})
    except IOError:
        return None
    else:
        return(ac)    

def write_results(results_file, array, labels):
    """Write a Dakota results file from an input numpy array."""
    try:
        with open(results_file, 'w') as fp:
            for i in range(len(array)):
                fp.write('{0s}\t{1}\n'.format(array[i], labels[i]))
    except IOError:
        raise
