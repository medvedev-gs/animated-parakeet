from typing import Optional, List

from core.interfaces.readers import IDataReader
from core.interfaces.dataframe import IDataFrame
from core.interfaces.config.models import IFileSettings


class ParquetReader(IDataReader):
    def __init__(self, file_settings: IFileSettings, engine='pandas'):
        self._file_settings = file_settings
        self._engine = engine

    @property
    def file_settings(self) -> IFileSettings:
        return self._file_settings

    @property
    def engine(self):
        return self._engine

    def read(self, usecols: Optional[List[str]] = None) -> IDataFrame:
        if self.engine == 'pandas':
            import pandas as pd
            return pd.read_parquet(
                path=self.file_settings.file_path,
                columns=usecols
            )
        raise NotImplementedError
