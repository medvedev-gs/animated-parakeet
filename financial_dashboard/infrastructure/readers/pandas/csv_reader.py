from pathlib import Path
from typing import Optional, List

from financial_dashboard.core.interfaces.readers import IDataReader
from financial_dashboard.core.interfaces.config.models import IParseSettings
from financial_dashboard.core.interfaces.dataframe import IDataFrame

from financial_dashboard.infrastructure.dataframes.pandas import PandasDataFrame


class CsvReader(IDataReader):
    def __init__(self, file_path: Path, parse_settings: IParseSettings) -> None:
        self._file_path = file_path
        self._parse_settings = parse_settings

    def read(self, usecols: Optional[List[str]] = None) -> IDataFrame:
        import pandas as pd
        return PandasDataFrame(data=pd.read_csv(
            self._file_path,
            usecols=usecols,
            sep=self._parse_settings.sep,
            skiprows=self._parse_settings.skip_rows,
            header=self._parse_settings.header,
            names=self._parse_settings.columns,
            dtype=self._parse_settings.dtypes,
            na_values=self._parse_settings.na_values,
            decimal=self._parse_settings.decimal,
            parse_dates=self._parse_settings.parse_dates,
            date_format=self._parse_settings.date_format,
            index_col=self._parse_settings.index_col,
            iterator=self._parse_settings.iterator,
            chunksize=self._parse_settings.chunksize
        ))
