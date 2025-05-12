from core.interfaces.dataframe import IDataFrame, PandasDataFrame, PolarsDataFrame


class BaseReader:
    def __init__(self, engine: str = "pandas"):
        self._engine = engine

    def _convert(self, raw_data) -> IDataFrame:
        if self._engine == "pandas":
            return PandasDataFrame(raw_data)
        if self._engine == "polars":
            return PolarsDataFrame(raw_data)
        raise NotImplementedError


class CsvReader(BaseReader):
    def read(self, path: str) -> IDataFrame:
        if self._engine == "pandas":
            import pandas as pd
            data = pd.read_csv(path)
        if self._engine == "polars":
            import polars as pl
            data = pl.read_csv(path)
        return self._convert(data)
