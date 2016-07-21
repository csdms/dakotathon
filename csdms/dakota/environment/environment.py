"""A class for top-level Dakota settings."""

classname = 'Environment'


class Environment(object):

    """Describe Dakota environment."""

    def __init__(self, data_file='dakota.dat', **kwargs):
        """Create a set of default experiment parameters."""
        self.data_file = data_file

    def __str__(self):
        """Define the environment block of a Dakota input file."""
        s = 'environment\n' \
            + '  tabular_data\n' \
            + '    tabular_data_file = {!r}\n\n'.format(self.data_file)
        return(s)
