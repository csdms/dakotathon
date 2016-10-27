"""Test the sampling method with the built-in *rosenbrock* function."""

import os
import filecmp
from nose.tools import assert_true
from dakotathon.dakota import Dakota
from . import data_dir


run_dir = os.getcwd()
input_file = os.path.join(run_dir, 'dakota.in')
known_input_file = os.path.join(data_dir, 'rosenbrock_sampling.in')
config_file = os.path.join(run_dir, 'dakota.yaml')
known_config_file = os.path.join(data_dir, 'default_sampling_dakota.yaml')


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global d
    d = Dakota(method='sampling', variables='uniform_uncertain')


def teardown_module():
    """Called after all tests have completed."""
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(config_file):
        os.remove(config_file)


def test_create_input_file():
    """Test whether a known input file can be matched."""
    d.write_input_file(input_file)
    assert_true(filecmp.cmp(known_input_file, input_file))


# XXX: Bad idea -- file contains full paths, which can't be matched on Travis.
# def test_create_config_file():
#     """Test whether a known config file can be matched."""
#     d.serialize(config_file)
#     assert_true(filecmp.cmp(known_config_file, config_file))

