# CSDMS Dakota interface examples

A set of [Jupyter Notebooks](http://jupyter.org/)
demonstrate how the CSDMS Dakota interface (CDI)
can be used.

From this directory,
start a Jupyter Notebook:

    $ jupyter notebook

and select one of the Notebooks to run.

The scripts

* **pymt-frostnumbermodel-vector-parameter-study.py**,
* **pymt-frostnumbermodel-multidim-parameter-study.py**, and
* **pymt-hydrotrend-centered-parameter-study.py**

demonstrate how the CDI can be called as a component
using [PyMT](https://github.com/csdms/pymt).
These scripts can be run on a WMT executor
in which the CDI has been installed,
as well as the [FrostNumberModel](https://github.com/permamodel/permamodel)
and [Hydrotrend](https://github.com/kettner/hydrotrend),
components.
For example:

    $ python pymt-frostnumbermodel-vector-parameter-study.py
