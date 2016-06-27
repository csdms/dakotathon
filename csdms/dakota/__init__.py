"""A Python interface to the Dakota iterative systems analysis toolkit."""
from .core import Dakota
from .bmi_dakota import BmiDakota


__all__ = ['Dakota', 'BmiDakota']
__version__ = '0.2'
