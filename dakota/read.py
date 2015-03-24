#! /usr/bin/env python
#
# Dakota utility programs for reading output.
#
# Mark Piper (mark.piper@colorado.edu)

import re


def get_labels(params_file):
    '''
    Uses a regular expression to extract labels from a Dakota parameters file.
    '''
    labels = []
    try:
        fp = open(params_file, 'r')
        for line in fp:
            if re.search('ASV_', line):
                labels.append(''.join(re.findall(':(\S+)', line)))
    except IOError:
        raise
    finally:
        fp.close()
        return(labels)
