#!/usr/bin/env python
import os
import yaml
from nose.tools import *
from dakota.bmi_dakota import BmiDakota
from dakota.utils import is_dakota_installed


config_val = {'method': 'vector_parameter_study', 'component': 'hydrotrend'}
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
    model = BmiDakota()
    name = model.get_component_name()
    assert_equal(name, 'Dakota')
    assert_is(model.get_component_name(), name)


@with_setup(setup, teardown)
def test_initialize_defaults():
    model = BmiDakota()
    model.initialize()
    assert_true(os.path.exists(input_file))


@with_setup(setup, teardown)
def test_initialize_from_file_like():
    from StringIO import StringIO

    config = StringIO(yaml.dump(config_val))
    model = BmiDakota()
    model.initialize(config)
    assert_true(os.path.exists(input_file))


@with_setup(setup, teardown)
def test_initialize_from_file():
    import tempfile

    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        fp.write(yaml.dump(config_val))
        fname = fp.name

    model = BmiDakota()
    model.initialize(fname)
    os.remove(fname)
    assert_true(os.path.exists(input_file))


def test_update():
    if is_dakota_installed():
        model = BmiDakota()
        model.initialize()
        model.update()
        assert_true(os.path.exists(input_file))
        assert_true(os.path.exists(output_file))
        assert_true(os.path.exists(data_file))


def test_finalize():
    if is_dakota_installed():
        model = BmiDakota()
        model.initialize()
        model.update()
        model.finalize()
