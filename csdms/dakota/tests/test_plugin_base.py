# Tests for dakota.plugins.base module.
#
# Call with:
#   $ nosetests -sv
#
# Mark Piper (mark.piper@colorado.edu)

from nose.tools import raises, assert_is_none
from csdms.dakota.plugins.base import PluginBase
from . import start_dir, data_dir

# Helpers --------------------------------------------------------------


class Concrete(PluginBase):

    """A subclass of PluginBase used for testing."""

    def __init__(self):
        PluginBase.__init__(self)

    def setup(self):
        return PluginBase.setup(self, None)

    def call(self):
        return PluginBase.call(self)

    def load(self):
        return PluginBase.load(self, None)

    def calculate(self):
        return PluginBase.calculate(self)

    def write(self):
        return PluginBase.write(self, None, None)

# Fixtures -------------------------------------------------------------


def setup_module():
    """Called before any tests are performed."""
    print('\n*** ' + __name__)
    global c
    c = Concrete()


def teardown_module():
    """Called after all tests have completed."""
    pass

# Tests ----------------------------------------------------------------


@raises(TypeError)
def test_instantiate():
    """Test whether PluginBase fails to instantiate."""
    d = PluginBase()


def test_setup():
    """Test type of setup method results."""
    s = c.setup()
    assert_is_none(s)


def test_call():
    """Test type of call method results."""
    s = c.call()
    assert_is_none(s)


def test_load():
    """Test type of load method results."""
    s = c.load()
    assert_is_none(s)


def test_calculate():
    """Test type of calculate method results."""
    s = c.calculate()
    assert_is_none(s)


def test_write():
    """Test type of write method results."""
    s = c.write()
    assert_is_none(s)
