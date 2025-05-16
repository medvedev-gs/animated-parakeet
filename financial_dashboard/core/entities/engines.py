from enum import Enum


class Engines(str, Enum):
    PANDAS = 'pandas'
    POLARS = 'polars'
