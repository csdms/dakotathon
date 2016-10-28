"""An example of using Dakota as a component with PyMT.

This example requires a WMT executor with PyMT installed, as well as
the CSDMS Dakota interface and FrostNumberModel installed as
components.

"""
import os
from pymt.components import VectorParameterStudy, FrostNumberModel
from dakotathon.utils import configure_parameters


c, d = FrostNumberModel(), VectorParameterStudy()

parameters = {
    'component': type(c).__name__,
    'descriptors': 'T_air_min',
    'initial_point': -10.0,
    'final_point': -5.0,
    'n_steps': 5,
    'response_descriptors': 'frostnumber__air',
    'response_statistics': 'median',
    }

parameters, substitutes = configure_parameters(parameters)

work_dir = c.setup(os.getcwd(), **substitutes)

cfg_file = 'frostnumber_model.cfg'  # get from pymt eventually
dtmpl_file = cfg_file + '.dtmpl'
os.rename(cfg_file, dtmpl_file)
parameters['template_file'] = os.path.join(work_dir, dtmpl_file)

d.setup(work_dir, **parameters)

d.initialize(os.path.join(work_dir, 'dakota.yaml'))
d.update()
d.finalize()

