#!/usr/bin/env python
#
# Tests for dakota.dakota_base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

import os
import filecmp
from nose.tools import *
from dakota.dakota_base import DakotaBase


# Fixtures -------------------------------------------------------------

def setup_module():
    """Called before any tests are performed."""
    print('\n*** DakotaBase tests')

def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------

@raises(TypeError)
def test_instantiate():
    """Test whether DakotaBase fails to instantiate."""
    d = DakotaBase()
