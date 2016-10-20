"""Unit tests for modules in the dakota package."""
import os

start_dir = os.path.dirname(__file__)
data_dir = os.path.join(start_dir, 'data')

dakota_files = {
    'input': 'dakota.in',
    'output': 'dakota.out',
    'data': 'dakota.dat',
    'restart': 'dakota.rst',
}
