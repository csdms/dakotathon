[![Build Status](https://travis-ci.org/csdms/dakota.svg?branch=master)](https://travis-ci.org/csdms/dakota)
[![Code Health](https://landscape.io/github/csdms/dakota/master/landscape.svg?style=flat)](https://landscape.io/github/csdms/dakota/master)

# CSDMS Dakota interface

The CSDMS Dakota interface provides
a [Basic Modeling Interface](http://dx.doi.org/10.1016/j.cageo.2012.04.002)
and API for the [Dakota](https://dakota.sandia.gov/)
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

	>>> from dakota.dakota import Dakota

Create a `Dakota` instance,
specifying the Dakota analysis method:

	>>> d = Dakota(method='vector_parameter_study')

Currently,
one Dakota method,
[vector parameter study](https://dakota.sandia.gov/sites/default/files/docs/6.0/html-ref/method-vector_parameter_study.html),
is supported.

To run a sample case,
create an input file
from the default vector parameter study values
and call Dakota:

	>>> d.write_input_file()
	>>> d.run()

Dakota output is written to two files
in the current directory,
**dakota.out** and **dakota.dat**.
