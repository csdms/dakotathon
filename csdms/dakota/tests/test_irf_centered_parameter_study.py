#!/usr/bin/env python
import os
import yaml
from nose.tools import assert_is, assert_true, assert_equal, with_setup
from csdms.dakota.bmi import CenteredParameterStudy
from csdms.dakota.utils import is_dakota_installed


config_val = {'method': 'centered_parameter_study'}
input_file, \
    output_file, \
    data_file, \
    restart_file = ['dakota.' + ext for ext in ('in', 'out', 'dat', 'rst')]


def setup():
    """Called at start of any test @with_setup()"""
    pass


def teardown():
    """Called at end of any test @with_setup()"""
    for f in [input_file, output_file, data_file, restart_file]:
        if os.path.exists(f):
            os.remove(f)


def test_component_name():
    model = CenteredParameterStudy()
    name = model.get_component_name()
    assert_equal(name, 'CenteredParameterStudy')
    assert_is(model.get_component_name(), name)


def test_start_time():
    model = CenteredParameterStudy()
    model.initialize()
    assert_equal(model.get_start_time(), 0.0)


def test_end_time():
    model = CenteredParameterStudy()
    model.initialize()
    assert_equal(model.get_end_time(), 1.0)


def test_current_time():
    model = CenteredParameterStudy()
    assert_equal(model.get_current_time(), 0.0)


def test_time_step():
    model = CenteredParameterStudy()
    assert_equal(model.get_time_step(), 1.0)


@with_setup(setup, teardown)
def test_initialize_defaults():
    model = CenteredParameterStudy()
    model.initialize()
    assert_true(os.path.exists(input_file))


@with_setup(setup, teardown)
def test_initialize_from_file_like():
    from StringIO import StringIO

    config = StringIO(yaml.dump(config_val))
    model = CenteredParameterStudy()
    model.initialize(config)
    assert_true(os.path.exists(input_file))


@with_setup(setup, teardown)
def test_initialize_from_file():
    import tempfile

    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        fp.write(yaml.dump(config_val))
        fname = fp.name

    model = CenteredParameterStudy()
    model.initialize(fname)
    os.remove(fname)
    assert_true(os.path.exists(input_file))


def test_update():
    if is_dakota_installed():
        model = CenteredParameterStudy()
        model.initialize()
        model.update()
        assert_true(os.path.exists(input_file))
        assert_true(os.path.exists(output_file))
        assert_true(os.path.exists(data_file))


def test_finalize():
    if is_dakota_installed():
        model = CenteredParameterStudy()
        model.initialize()
        model.update()
        model.finalize()
