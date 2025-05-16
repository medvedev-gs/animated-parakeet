import pandas as pd

from financial_dashboard.core.interfaces.dataframe import IDataFrame


class PandasDataFrame(IDataFrame):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    def filter_rows(self, condition) -> 'IDataFrame':
        return PandasDataFrame(self._data[condition])
