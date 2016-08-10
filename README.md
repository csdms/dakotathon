[![Build Status](https://travis-ci.org/csdms/dakota.svg?branch=master)](https://travis-ci.org/csdms/dakota)
[![Code Health](https://landscape.io/github/csdms/dakota/master/landscape.svg?style=flat)](https://landscape.io/github/csdms/dakota/master)
[![Coverage Status](https://coveralls.io/repos/csdms/dakota/badge.svg?branch=master)](https://coveralls.io/r/csdms/dakota?branch=master)
[![Documentation Status](https://readthedocs.org/projects/csdms-dakota/badge/?version=latest)](https://readthedocs.org/projects/csdms-dakota/?badge=latest)

# CSDMS Dakota interface

The CSDMS Dakota interface provides
a [Basic Model Interface](http://dx.doi.org/10.1016/j.cageo.2012.04.002)
and a Python API for the [Dakota](https://dakota.sandia.gov/)
iterative systems analysis toolkit.
This is currently alpha-level software
supported on Linux and Mac OSX.

## Installation

Install the CSDMS Dakota interface with:

	$ git clone https://github.com/csdms/dakota.git
	$ cd dakota
	$ python setup.py install

The CSDMS Dakota interface requires Dakota.
Follow the instructions on the Dakota website
for [downloading](https://dakota.sandia.gov/download.html) and
[installing](https://dakota.sandia.gov/content/install-linux-macosx)
a precompiled Dakota binary for your system.
Dakota version 6.1 is supported by the CSDMS Dakota interface.

HydroTrend is the only CSDMS model currently supported
in the CSDMS Dakota interface.
On Mac OS X,
install HydroTrend through [Homebrew](http://brew.sh/):

	$ brew tap csdms/models
	$ brew install hydrotrend

On Linux,
build HydroTrend from source:

	$ git clone https://github.com/csdms-contrib/hydrotrend.git
	$ mkdir -p hydrotrend/build && cd hydrotrend/build
	$ cmake ..
	$ make
	$ make install

## Execution

Import the CSDMS Dakota interface into a Python session with:

	>>> from csdms.dakota import Dakota

Create a `Dakota` instance,
specifying a Dakota analysis method:

	>>> d = Dakota(method='vector_parameter_study')

Currently,
six Dakota methods

* [vector_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-vector_parameter_study.html)
* [centered_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-centered_parameter_study.html)
* [multidim_parameter_study](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-multidim_parameter_study.html)
* [sampling](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-sampling.html)
* [polynomial_chaos](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-polynomial_chaos.html)
* [stoch_collocation](https://dakota.sandia.gov/sites/default/files/docs/6.1/html-ref/method-stoch_collocation.html)

are supported.

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
see the Jupyter Notebooks in the [examples](./examples) directory
of this repository.


### Note

If you're using Anaconda IPython on Mac OS X,
include the `DYLD_LIBRARY_PATH` environment variable
in your session before calling the `run` method with:

```python
>>> from csdms.dakota.utils import add_dyld_library_path
>>> add_dyld_library_path()
```

See https://github.com/csdms/dakota/issues/17 for more information.
