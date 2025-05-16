import polars as pl

from financial_dashboard.core.interfaces.dataframe import IDataFrame


class PolarsDataFrame(IDataFrame):
    def __init__(self, data: pl.DataFrame):
        self._data = data

    def filter_rows(self, condition) -> 'IDataFrame':
        return PolarsDataFrame(self._data.filter(condition))
