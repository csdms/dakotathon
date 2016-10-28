# CSDMS Dakota interface examples

A set of [Jupyter Notebooks](http://jupyter.org/)
demonstrate how the CSDMS Dakota interface (CDI)
can be used.

From this directory,
start a Jupyter Notebook:

    $ jupyter notebook

and select one of the Notebooks to run.

The script **pymt-frostnumbermodel-vector-parameter-study.py**
demonstrates how the CDI can be called as a component
using [PyMT](https://github.com/csdms/pymt).
This script can be run on a WMT executor
in which the CDI
and the [FrostNumberModel](https://github.com/permamodel/permamodel)
have been installed as components:

    $ python pymt-frostnumbermodel-vector-parameter-study.py
