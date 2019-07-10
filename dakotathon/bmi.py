#!/usr/bin/env python
"""Basic Model Interface for the Dakota iterative systems analysis toolkit."""

from bmipy import Bmi
from .dakota import Dakota


class BmiDakota(Bmi):

    """The BMI implementation for the CSDMS Dakota interface."""

    _name = "Dakota"

    def __init__(self):
        """Create a BmiDakota instance."""
        self._model = None
        self._time = 0.0

    def finalize(self):
        """Perform tear-down tasks for the model.

        Perform all tasks that take place after exiting the model's time
        loop. This typically includes deallocating memory, closing files and
        printing reports.
        """
        self._model = None

    def get_component_name(self):
        """Name of the component.

        Returns
        -------
        str
            The name of the component.
        """
        return self._name

    def get_current_time(self):
        """Current time of the model.

        Returns
        -------
        float
            The current model time.
        """
        return self._time

    def get_end_time(self):
        """End time of the model.

        Returns
        -------
        float
            The maximum model time.
        """
        return 1.0

    def get_grid_edge_count(self, grid):
        """Get the number of edges in the grid.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        int
            The total number of grid edges.
        """
        raise NotImplementedError("get_grid_edge_count")

    def get_grid_edge_nodes(self, grid, edge_nodes):
        """Get the edge-node connectivity.

        Parameters
        ----------
        grid : int
            A grid identifier.
        edge_nodes : ndarray of int, shape *(2 x nnodes,)*
            A numpy array to place the edge-node connectivity. For each edge,
            connectivity is given as node at edge tail, followed by node at
            edge head.

        Returns
        -------
        ndarray of int
            The input numpy array that holds the edge-node connectivity.
        """
        raise NotImplementedError("get_grid_edge_nodes")

    def get_grid_face_count(self, grid):
        """Get the number of faces in the grid.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        int
            The total number of grid faces.
        """
        raise NotImplementedError("get_grid_face_count")

    def get_grid_face_nodes(self, grid, face_nodes):
        """Get the face-node connectivity.

        Parameters
        ----------
        grid : int
            A grid identifier.
        face_nodes : ndarray of int
            A numpy array to place the face-node connectivity. For each face,
            the nodes (listed in a counter-clockwise direction) that form the
            boundary of the face.

        Returns
        -------
        ndarray of int
            The input numpy array that holds the face-node connectivity.
        """
        raise NotImplementedError("get_grid_face_nodes")

    def get_grid_node_count(self, grid):
        """Get the number of nodes in the grid.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        int
            The total number of grid nodes.
        """
        raise NotImplementedError("get_grid_node_count")

    def get_grid_nodes_per_face(self, grid, nodes_per_face):
        """Get the number of nodes for each face.

        Parameters
        ----------
        grid : int
            A grid identifier.
        nodes_per_face : ndarray of int, shape *(nfaces,)*
            A numpy array to place the number of edges per face.

        Returns
        -------
        ndarray of int
            The input numpy array that holds the number of nodes per edge.
        """
        raise NotImplementedError("get_grid_nodes_per_face")

    def get_grid_origin(self, grid, origin):
        """Get coordinates for the lower-left corner of the computational grid.

        Parameters
        ----------
        grid : int
            A grid identifier.
        origin : ndarray of float, shape *(ndim,)*
            A numpy array to hold the coordinates of the lower-left corner of
            the grid.

        Returns
        -------
        ndarray of float
            The input numpy array that holds the coordinates of the grid's
            lower-left corner.
        """
        raise NotImplementedError("get_grid_origin")

    def get_grid_rank(self, grid):
        """Get number of dimensions of the computational grid.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        int
            Rank of the grid.
        """
        raise NotImplementedError("get_grid_rank")

    def get_grid_shape(self, grid, shape):
        """Get dimensions of the computational grid.

        Parameters
        ----------
        grid : int
            A grid identifier.
        shape : ndarray of int, shape *(ndim,)*
            A numpy array into which to place the shape of the grid.

        Returns
        -------
        ndarray of int
            The input numpy array that holds the grid's shape.
        """
        raise NotImplementedError("get_grid_shape")

    def get_grid_size(self, grid):
        """Get the total number of elements in the computational grid.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        int
            Size of the grid.
        """
        raise NotImplementedError("get_grid_size")

    def get_grid_spacing(self, grid, spacing):
        """Get distance between nodes of the computational grid.

        Parameters
        ----------
        grid : int
            A grid identifier.
        spacing : ndarray of float, shape *(ndim,)*
            A numpy array to hold the spacing between grid rows and columns.

        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's spacing.
        """
        raise NotImplementedError("get_grid_spacing")

    def get_grid_type(self, grid):
        """Get the grid type as a string.

        Parameters
        ----------
        grid : int
            A grid identifier.

        Returns
        -------
        str
            Type of grid as a string.
        """
        raise NotImplementedError("get_grid_type")

    def get_grid_x(self, grid, x):
        """Get coordinates of grid nodes in the x direction.

        Parameters
        ----------
        grid : int
            A grid identifier.
        x : ndarray of float, shape *(nrows,)*
            A numpy array to hold the x-coordinates of the grid node columns.

        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's column x-coordinates.
        """
        raise NotImplementedError("get_grid_x")

    def get_grid_y(self, grid, y):
        """Get coordinates of grid nodes in the y direction.

        Parameters
        ----------
        grid : int
            A grid identifier.
        y : ndarray of float, shape *(ncols,)*
            A numpy array to hold the y-coordinates of the grid node rows.

        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's row y-coordinates.
        """
        raise NotImplementedError("get_grid_y")

    def get_grid_z(self, grid, z):
        """Get coordinates of grid nodes in the z direction.

        Parameters
        ----------
        grid : int
            A grid identifier.
        z : ndarray of float, shape *(nlayers,)*
            A numpy array to hold the z-coordinates of the grid nodes layers.

        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's layer z-coordinates.
        """
        raise NotImplementedError("get_grid_z")

    def get_input_var_names(self):
        """List of a model's input variables.

        Input variable names must be CSDMS Standard Names, also known
        as *long variable names*.

        Returns
        -------
        list of str
            The input variables for the model.

        Notes
        -----
        Standard Names enable the CSDMS framework to determine whether
        an input variable in one model is equivalent to, or compatible
        with, an output variable in another model. This allows the
        framework to automatically connect components.

        Standard Names do not have to be used within the model.
        """
        raise NotImplementedError("get_input_var_names")

    def get_output_var_names(self):
        """List of a model's output variables.

        Output variable names must be CSDMS Standard Names, also known
        as *long variable names*.

        Returns
        -------
        list of str
            The output variables for the model.
        """
        raise NotImplementedError("get_output_var_names")

    def get_start_time(self):
        """Start time of the model.

        Model times should be of type float.

        Returns
        -------
        float
            The model start time.
        """
        return 0.0

    def get_time_step(self):
        """Current time step of the model.

        The model time step should be of type float.

        Returns
        -------
        float
            The time step used in model.
        """
        return 1.0

    def get_time_units(self):
        """Time units of the model.

        Returns
        -------
        float
            The model time unit; e.g., `days` or `s`.

        Notes
        -----
        CSDMS uses the UDUNITS standard from Unidata.
        """
        raise NotImplementedError("get_time_units")

    def get_value(self, name, dest):
        """Get a copy of values of the given variable.

        This is a getter for the model, used to access the model's
        current state. It returns a *copy* of a model variable, with
        the return type, size and rank dependent on the variable.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        dest : ndarray
            A numpy array into which to place the values.

        Returns
        -------
        ndarray
            The same numpy array that was passed as an input buffer.
        """
        raise NotImplementedError("get_value")

    def get_value_at_indices(self, name, dest, inds):
        """Get values at particular indices.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        dest : ndarray
            A numpy array into which to place the values.
        indices : array_like
            The indices into the variable array.

        Returns
        -------
        array_like
            Value of the model variable at the given location.
        """
        raise NotImplementedError("get_value_at_indices")

    def get_value_ptr(self, name):
        """Get a reference to values of the given variable.

        This is a getter for the model, used to access the model's
        current state. It returns a reference to a model variable,
        with the return type, size and rank dependent on the variable.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        array_like
            A reference to a model variable.
        """
        raise NotImplementedError("get_value_ptr")

    def get_var_grid(self, name):
        """Get grid identifier for the given variable.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        int
          The grid identifier.
        """
        raise NotImplementedError("get_var_grid")

    def get_var_itemsize(self, name):
        """Get memory use for each array element in bytes.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        int
            Item size in bytes.
        """
        raise NotImplementedError("get_var_itemsize")

    def get_var_location(self, name):
        """Get the grid element type that the a given variable is defined on.

        The grid topology can be composed of *nodes*, *edges*, and *faces*.

        *node*
            A point that has a coordinate pair or triplet: the most
            basic element of the topology.

        *edge*
            A line or curve bounded by two *nodes*.

        *face*
            A plane or surface enclosed by a set of edges. In a 2D
            horizontal application one may consider the word "polygon",
            but in the hierarchy of elements the word "face" is most common.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        str
            The grid location on which the variable is defined. Must be one of
            `"node"`, `"edge"`, or `"face"`.

        Notes
        -----
        CSDMS uses the `ugrid conventions`_ to define unstructured grids.

        .. _ugrid conventions: http://ugrid-conventions.github.io/ugrid-conventions
        """
        raise NotImplementedError("get_var_location")

    def get_var_nbytes(self, name):
        """Get size, in bytes, of the given variable.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        int
            The size of the variable, counted in bytes.
        """
        raise NotImplementedError("get_var_nbytes")

    def get_var_type(self, name):
        """Get data type of the given variable.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        str
            The Python variable type; e.g., ``str``, ``int``, ``float``.
        """
        raise NotImplementedError("get_var_type")

    def get_var_units(self, name):
        """Get units of the given variable.

        Standard unit names, in lower case, should be used, such as
        ``meters`` or ``seconds``. Standard abbreviations, like ``m`` for
        meters, are also supported. For variables with compound units,
        each unit name is separated by a single space, with exponents
        other than 1 placed immediately after the name, as in ``m s-1``
        for velocity, ``W m-2`` for an energy flux, or ``km2`` for an
        area.

        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.

        Returns
        -------
        str
            The variable units.

        Notes
        -----
        CSDMS uses the `UDUNITS`_ standard from Unidata.

        .. _UDUNITS: http://www.unidata.ucar.edu/software/udunits
        """
        raise NotImplementedError("get_var_units")

    def initialize(self, config_file):
        """Perform startup tasks for the model.

        Perform all tasks that take place before entering the model's time
        loop, including opening files and initializing the model state. Model
        inputs are read from a text-based configuration file, specified by
        `filename`.

        Parameters
        ----------
        config_file : str, optional
            The path to the model configuration file.

        Notes
        -----
        Models should be refactored, if necessary, to use a
        configuration file. CSDMS does not impose any constraint on
        how configuration files are formatted, although YAML is
        recommended. A template of a model's configuration file
        with placeholder values is used by the BMI.
        """
        if config_file is None:
            self._model = Dakota()
        else:
            self._model = Dakota.from_file_like(config_file)

        self._model.write_input_file()

    def set_value(self, name, values):
        """Specify a new value for a model variable.

        This is the setter for the model, used to change the model's
        current state. It accepts, through *src*, a new value for a
        model variable, with the type, size and rank of *src*
        dependent on the variable.

        Parameters
        ----------
        var_name : str
            An input or output variable name, a CSDMS Standard Name.
        src : array_like
            The new value for the specified variable.
        """
        raise NotImplementedError("set_value")

    def set_value_at_indices(self, name, inds, src):
        """Specify a new value for a model variable at particular indices.

        Parameters
        ----------
        var_name : str
            An input or output variable name, a CSDMS Standard Name.
        indices : array_like
            The indices into the variable array.
        src : array_like
            The new value for the specified variable.
        """
        raise NotImplementedError("set_value_at_indices")

    def update(self):
        """Advance model state by one time step.

        Perform all tasks that take place within one pass through the model's
        time loop. This typically includes incrementing all of the model's
        state variables. If the model's state variables don't change in time,
        then they can be computed by the :func:`initialize` method and this
        method can return with no action.
        """
        self._model.run()
        self._time += self.get_time_step()


class CenteredParameterStudy(BmiDakota):

    """BMI implementation of a Dakota centered parameter study."""

    _name = "CenteredParameterStudy"

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method="centered_parameter_study")
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class MultidimParameterStudy(BmiDakota):

    """BMI implementation of a Dakota multidim parameter study."""

    _name = "MultidimParameterStudy"

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method="multidim_parameter_study")
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class VectorParameterStudy(BmiDakota):

    """BMI implementation of a Dakota vector parameter study."""

    _name = "VectorParameterStudy"

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method="vector_parameter_study")
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class Sampling(BmiDakota):

    """BMI implementation of a Dakota sampling study."""

    _name = "Sampling"

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(method="sampling", variables="uniform_uncertain")
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class PolynomialChaos(BmiDakota):

    """BMI implementation of a Dakota study with the polynomial chaos method."""

    _name = "PolynomialChaos"

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(
                method="polynomial_chaos", variables="uniform_uncertain"
            )
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class StochasticCollocation(BmiDakota):

    """BMI implementation of a Dakota study with the stochastic collocation method."""

    _name = "StochasticCollocation"

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.

        Parameters
        ----------
        filename : str, optional
            Path to a Dakota configuration file.

        """
        if filename is None:
            self._model = Dakota(
                method="stoch_collocation", variables="uniform_uncertain"
            )
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()


class PsuadeMoat(BmiDakota):

    """BMI implementation of a Dakota study with the PSUADE MOAT method."""

    _name = "PsuadeMoat"

    def initialize(self, filename=None):
        """Create a Dakota instance and input file.
            
            Parameters
            ----------
            filename : str, optional
            Path to a Dakota configuration file.
            
            """
        if filename is None:
            self._model = Dakota(method="psuade_moat", variables="uniform_uncertain")
        else:
            self._model = Dakota.from_file_like(filename)

        self._model.write_input_file()
