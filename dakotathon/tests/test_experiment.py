"""Tests for the dakotathon.experiment module."""

import os
from nose.tools import (raises, assert_true, assert_equal,
                        assert_is_instance, assert_is_none,
                        assert_is_not_none)
from dakotathon.experiment import Experiment


def setup_module():
    """Fixture called before any tests are performed."""
    print('\n*** ' + __name__)
    global x
    x = Experiment()


def teardown_module():
    """Fixture called after all tests have completed."""
    pass


def test_instantiate():
    """Test whether Experiment instantiates."""
    e = Experiment()


def test_get_component():
    """Test getting the component attribute."""
    assert_is_none(x.component)


def test_set_component():
    """Test setting the component attribute."""
    e = Experiment()
    component = 'hydrotrend'
    e.component = component
    assert_equal(e.component, component)


def test_component_sets_interface_type():
    """Test that setting component sets fork interface."""
    from .test_interface_fork import Fork
    component = 'hydrotrend'
    e = Experiment(component=component)
    assert_is_instance(e.interface, Fork)


def test_component_sets_analysis_driver():
    """Test that setting component sets the analysis driver."""
    component = 'hydrotrend'
    e = Experiment(component=component)
    assert_equal(e.interface.analysis_driver, 'dakota_run_component')


def test_get_plugin():
    """Test getting the plugin attribute."""
    assert_is_none(x.plugin)


def test_set_plugin():
    """Test setting the plugin attribute."""
    e = Experiment()
    plugin = 'hydrotrend'
    e.plugin = plugin
    assert_equal(e.plugin, plugin)


def test_plugin_sets_interface_type():
    """Test that setting plugin sets fork interface."""
    from .test_interface_fork import Fork
    plugin = 'hydrotrend'
    e = Experiment(plugin=plugin)
    assert_is_instance(e.interface, Fork)


def test_plugin_sets_analysis_driver():
    """Test that setting plugin sets the analysis driver."""
    plugin = 'hydrotrend'
    e = Experiment(plugin=plugin)
    assert_equal(e.interface.analysis_driver, 'dakota_run_plugin')


@raises(AttributeError)
def test_setting_component_and_plugin():
    """Test that setting component and plugin raises exception."""
    component = plugin = 'hydrotrend'
    e = Experiment(component=component, plugin=plugin)


def test_multidim_parameter_study_uses_bounds():
    """Test that the multidim parameter study uses bounds."""
    e = Experiment(method='multidim_parameter_study')
    assert_is_not_none(e.variables.lower_bounds)
    assert_is_not_none(e.variables.upper_bounds)


def test_get_environment():
    """Test getting the environment property."""
    from .test_environment_base import EnvironmentBase
    assert_is_instance(x.environment, EnvironmentBase)


def test_set_environment():
    """Test setting the environment property."""
    from .test_environment_base import Concrete
    e = Experiment()
    inst = Concrete()
    e.environment = inst
    assert_equal(e.environment, inst)


@raises(TypeError)
def test_set_environment_fails_if_not_instance():
    """Test that environment fails with a non-instance input."""
    e = Experiment()
    answer = 42
    e.environment = answer


def test_get_method():
    """Test getting the method property."""
    from .test_method_base import MethodBase
    assert_is_instance(x.method, MethodBase)


def test_set_method():
    """Test setting the method property."""
    from .test_method_base import Concrete
    e = Experiment()
    inst = Concrete()
    e.method = inst
    assert_equal(e.method, inst)


@raises(TypeError)
def test_set_method_fails_if_not_instance():
    """Test that method fails with a non-instance input."""
    e = Experiment()
    answer = 42
    e.method = answer


def test_get_variables():
    """Test getting the variables property."""
    from .test_variables_base import VariablesBase
    assert_is_instance(x.variables, VariablesBase)


def test_set_variables():
    """Test setting the variables property."""
    from .test_variables_base import Concrete
    e = Experiment()
    inst = Concrete()
    e.variables = inst
    assert_equal(e.variables, inst)


@raises(TypeError)
def test_set_variables_fails_if_not_instance():
    """Test that variables fails with a non-instance input."""
    e = Experiment()
    answer = 42
    e.variables = answer


def test_get_interface():
    """Test getting the interface property."""
    from .test_interface_base import InterfaceBase
    assert_is_instance(x.interface, InterfaceBase)


def test_set_interface():
    """Test setting the interface property."""
    from .test_interface_base import Concrete
    e = Experiment()
    inst = Concrete()
    e.interface = inst
    assert_equal(e.interface, inst)


@raises(TypeError)
def test_set_interface_fails_if_not_instance():
    """Test that interface fails with a non-instance input."""
    e = Experiment()
    answer = 42
    e.interface = answer


def test_get_responses():
    """Test getting the responses property."""
    from .test_responses_base import ResponsesBase
    assert_is_instance(x.responses, ResponsesBase)


def test_set_responses():
    """Test setting the responses property."""
    from .test_responses_base import Concrete
    e = Experiment()
    inst = Concrete()
    e.responses = inst
    assert_equal(e.responses, inst)


@raises(TypeError)
def test_set_responses_fails_if_not_instance():
    """Test that responses fails with a non-instance input."""
    e = Experiment()
    answer = 42
    e.responses = answer


def test_str_special():
    """Test type of __str__ method results."""
    s = str(x)
    assert_true(type(s) is str)


def test_str_length():
    """Test the default length of __str__."""
    x = Experiment()
    s = str(x)
    n_lines = len(s.splitlines())
    assert_equal(n_lines, 25)

