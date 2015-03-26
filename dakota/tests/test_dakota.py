#!/usr/bin/env python
#
# Tests for dakota.dakota module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import *
from dakota.dakota import Dakota

def setup_module():
    print('Dakota tests:')
    global d
    d = Dakota()

def teardown_module():
    pass

def test_run():
    """Test the run method."""
    d.run()

def test_write():
    """Test the write method."""
    d.write()
