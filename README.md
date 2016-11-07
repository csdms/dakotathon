[![Build Status](https://travis-ci.org/csdms/dakota.svg?branch=master)](https://travis-ci.org/csdms/dakota)
[![Code Health](https://landscape.io/github/csdms/dakota/master/landscape.svg?style=flat)](https://landscape.io/github/csdms/dakota/master)
[![Coverage Status](https://coveralls.io/repos/csdms/dakota/badge.svg?branch=master)](https://coveralls.io/r/csdms/dakota?branch=master)
[![Documentation Status](https://readthedocs.org/projects/csdms-dakota/badge/?version=latest)](https://readthedocs.org/projects/csdms-dakota/?badge=latest)
[![Anaconda-Server Badge](https://anaconda.org/csdms/dakotathon/badges/version.svg)](https://anaconda.org/csdms/dakotathon)
[![Anaconda-Server Badge](https://anaconda.org/csdms/dakotathon/badges/installer/conda.svg)](https://conda.anaconda.org/csdms)
[![Anaconda-Server Badge](https://anaconda.org/csdms/dakotathon/badges/downloads.svg)](https://anaconda.org/csdms/dakotathon)

# CSDMS Dakota interface

The CSDMS Dakota interface (CDI) provides
a [Basic Model Interface](http://dx.doi.org/10.1016/j.cageo.2012.04.002)
and a Python API for a subset of the methods
included in the [Dakota](https://dakota.sandia.gov/)
iterative systems analysis toolkit,
including:

* [vector_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-vector_parameter_study.html),
* [centered_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-centered_parameter_study.html),
* [multidim_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-multidim_parameter_study.html),
* [sampling](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-sampling.html),
* [polynomial_chaos](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-polynomial_chaos.html), and
* [stoch_collocation](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-stoch_collocation.html).

This is currently alpha-level software
supported on Linux and Mac OSX.

## Installation

Install the CDI into a Anaconda Python distribution with

    $ conda install -c csdms dakotathon

or install from source with

	$ git clone https://github.com/csdms/dakota.git
	$ cd dakota
	$ python setup.py install

The CDI requires Dakota.
Follow the instructions on the Dakota website
for [downloading](https://dakota.sandia.gov/download.html) and
[installing](https://dakota.sandia.gov/content/install-linux-macosx)
a precompiled Dakota binary for your system.
Dakota version 6.1 is supported by the CSDMS Dakota interface.

## Execution: standalone

Import the CDI into a Python session with:

	>>> from dakotathon import Dakota

Create a `Dakota` instance,
specifying a Dakota analysis method:

	>>> d = Dakota(method='vector_parameter_study')

To run a sample case,
create a Dakota input file
from the default vector parameter study
and call Dakota:

	>>> d.write_input_file()
	>>> d.run()

Dakota output is written to two files,
**dakota.out** (run information)
and
**dakota.dat** (tabular output),
in the current directory.

For more in-depth examples of using the CSDMS Dakota interface,
see the Jupyter Notebooks
in the [examples](./examples) directory
of this repository.


### Note

If you're using Anaconda IPython on Mac OS X,
include the `DYLD_LIBRARY_PATH` environment variable
in your session before calling the `run` method with:

```python
>>> from dakotathon.utils import add_dyld_library_path
>>> add_dyld_library_path()
```

See https://github.com/csdms/dakota/issues/17 for more information.

## Execution: in PyMT

The CDI can also be called as a component in a WMT execution server
where [PyMT](https://github.com/csdms/pymt) has been installed.
For example,
to perform a centered parameter study on the Hydrotrend component,
start with imports:

```python
import os
from pymt.components import CenteredParameterStudy, Hydrotrend
from dakotathon.utils import configure_parameters
```

then create instances of the Hydrotrend and Dakota components:

```python
h, c = Hydrotrend(), CenteredParameterStudy()
```

Next,
set up a dict of parameters for the experiment:

```python
parameters = {
  'component': type(c).__name__,
  'run_duration': 365,               # days
  'auxiliary_files': 'HYDRO0.HYPS',  # the default Waipaoa hypsometry
  'descriptors': ['starting_mean_annual_temperature',
                  'total_annual_precipitation'],
  'initial_point': [15.0, 2.0],
  'steps_per_variable': [2, 5],
  'step_vector': [2.5, 0.2],
  'response_descriptors': ['channel_exit_water_sediment~suspended__mass_flow_rate',
                           'channel_exit_water__volume_flow_rate'],
  'response_statistics': ['median', 'mean']
}
```

and use a helper function
to format the parameters for Dakota and Hydrotrend:

```python
cparameters, hparameters = configure_parameters(parameters)
```

Set up the Hydrotrend component:

```python
cparameters['run_directory'] = h.setup(os.getcwd(), **hparameters)
```

Create the Dakota template file from the Hydrotrend input file:

```python
cfg_file = 'HYDRO.IN'  # get from pymt eventually
dtmpl_file = cfg_file + '.dtmpl'
os.rename(cfg_file, dtmpl_file)
cparameters['template_file'] = dtmpl_file
```

Set up the Dakota component:

```python
c.setup(dparameters['run_directory'], **cparameters)
```

then initialize, run, and finalize the Dakota component:

```python
c.initialize('dakota.yaml')
c.update()
c.finalize()
```

Dakota output is written to two files,
**dakota.out** (run information)
and
**dakota.dat** (tabular output),
in the current directory.

For more in-depth examples of using the CDI with PyMT,
see the Python scripts
in the [examples](./examples) directory
of this repository.
