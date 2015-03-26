#!/usr/bin/env python
#
# Tests for the dakota.vector_parameter_study module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import *
from dakota.vector_parameter_study import VectorParameterStudy

def setup_module():
    print('VectorParameterStudy tests:')
    global v
    v = VectorParameterStudy()

def teardown_module():
    pass

def test_run():
    """Test the run method."""
    v.run()

def test_write():
    """Test the write method."""
    v.write()
