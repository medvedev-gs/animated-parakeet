from pathlib import Path
from typing import Optional, List

from core.interfaces.readers import IDataReader
from financial_dashboard.core.interfaces.config.models import IParseSettings
from core.interfaces.dataframe import IDataFrame

from financial_dashboard.infrastructure.dataframes.pandas import PandasDataFrame


class ParquetReader(IDataReader):
    def __init__(self, file_path: Path, parse_settings: Optional[IParseSettings] = None):
        self._file_path = file_path
        self._parse_settings = parse_settings

    def read(self, usecols: Optional[List[str]] = None) -> IDataFrame:
        import pandas as pd
        return PandasDataFrame(data=pd.read_parquet(
            path=self._file_path,
            columns=usecols
        ))
