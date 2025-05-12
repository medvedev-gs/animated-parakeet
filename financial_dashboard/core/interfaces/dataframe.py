# core/interfaces/dataframe.py
from abc import ABC, abstractmethod
from typing import Union, Optional
import pandas as pd
import polars as pl


class IDataFrame(ABC):
    @abstractmethod
    def filter_rows(self, condition) -> 'IDataFrame': ...
    
    @abstractmethod
    def select_cols(self, columns: list[str]) -> 'IDataFrame': ...
    
    @abstractmethod
    def to_pandas(self) -> pd.DataFrame: ...
    
    @abstractmethod
    def to_polars(self) -> pl.DataFrame: ...


class PandasDataFrame(IDataFrame):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def filter_rows(self, condition) -> 'IDataFrame':
        return PandasDataFrame(self._data[condition])


class PolarsDataFrame(IDataFrame):
    def __init__(self, data: pl.DataFrame):
        self._data = data

    def filter_rows(self, condition) -> 'IDataFrame':
        return PolarsDataFrame(self._data.filter(condition))
