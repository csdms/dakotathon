"""An example of using Dakota as a component with PyMT.

This example requires a WMT executor with PyMT installed, as well as
the CSDMS Dakota interface and Hydrotrend installed as
components.

"""
import os
from pymt.components import CenteredParameterStudy, Hydrotrend
from dakotathon.utils import configure_parameters


c, d = Hydrotrend(), CenteredParameterStudy()

parameters = {
    'component': type(c).__name__,
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

parameters, substitutes = configure_parameters(parameters)

parameters['run_directory'] = c.setup(os.getcwd(), **substitutes)

cfg_file = 'HYDRO.IN'  # get from pymt eventually
dtmpl_file = cfg_file + '.dtmpl'
os.rename(cfg_file, dtmpl_file)
parameters['template_file'] = dtmpl_file

d.setup(parameters['run_directory'], **parameters)

d.initialize('dakota.yaml')
d.update()
d.finalize()

