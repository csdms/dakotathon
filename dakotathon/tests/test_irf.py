#!/usr/bin/env python
import os
import yaml
from nose.tools import assert_is, assert_true, assert_equal, with_setup
from dakotathon.bmi import BmiDakota
from dakotathon.utils import is_dakota_installed
from . import dakota_files


config_val = {'method': 'vector_parameter_study', 'component': 'hydrotrend'}


def setup():
    """Called at start of any test @with_setup()"""
    pass


def teardown():
    """Called at end of any test @with_setup()"""
    for f in list(dakota_files.values()):
        if os.path.exists(f):
            os.remove(f)


def test_component_name():
    model = BmiDakota()
    name = model.get_component_name()
    assert_equal(name, 'Dakota')
    assert_is(model.get_component_name(), name)


def test_start_time():
    model = BmiDakota()
    model.initialize(None)
    assert_equal(model.get_start_time(), 0.0)


def test_end_time():
    model = BmiDakota()
    model.initialize(None)
    assert_equal(model.get_end_time(), 1.0)


def test_current_time():
    model = BmiDakota()
    assert_equal(model.get_current_time(), 0.0)


def test_time_step():
    model = BmiDakota()
    assert_equal(model.get_time_step(), 1.0)


@with_setup(setup, teardown)
def test_initialize_defaults():
    model = BmiDakota()
    model.initialize(None)
    assert_true(os.path.exists(dakota_files['input']))


@with_setup(setup, teardown)
def test_initialize_from_file_like():
    from io import BytesIO
    
    config = BytesIO(yaml.dump(config_val, encoding=('utf-8')))
    model = BmiDakota()
    model.initialize(config)
    assert_true(os.path.exists(dakota_files['input']))


@with_setup(setup, teardown)
def test_initialize_from_file():
    import tempfile

    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        fp.write(yaml.dump(config_val))
        fname = fp.name

    model = BmiDakota()
    model.initialize(fname)
    os.remove(fname)
    assert_true(os.path.exists(dakota_files['input']))


def test_update():
    if is_dakota_installed():
        model = BmiDakota()
        model.initialize(None)
        model.update()
        assert_true(os.path.exists(dakota_files['input']))
        assert_true(os.path.exists(dakota_files['output']))
        assert_true(os.path.exists(dakota_files['data']))


def test_finalize():
    if is_dakota_installed():
        model = BmiDakota()
        model.initialize(None)
        model.update()
        model.finalize()
