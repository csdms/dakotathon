#! /usr/bin/env python
#
# Dakota utility programs for writing output.
#
# Mark Piper (mark.piper@colorado.edu)

def write_results(results_file, array, labels):
    '''
    Writes a Dakota results file from an input array.
    '''
    try:
        fp = open(results_file, 'w')
        for i in range(len(array)):
            fp.write(str(array[i]) + '\t' + labels[i] + '\n')
    except IOError:
        raise
    finally:
        fp.close()
