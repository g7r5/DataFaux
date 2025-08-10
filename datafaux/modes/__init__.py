"""
DataFaux modes package.

This package contains different execution modes for DataFaux:
- testers: Mode for generating test datasets
- streaming: Mode for streaming data generation
"""

from .testers import TestersMode
from .streaming import StreamingMode

__all__ = ['TestersMode', 'StreamingMode']
