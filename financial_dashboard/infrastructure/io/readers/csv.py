from typing import Optional, List

from core.interfaces.readers import IDataReader
from core.interfaces.config.models import IParseSettings, IFileSettings
from core.interfaces.dataframe import IDataFrame


class CsvReader(IDataReader):
    def __init__(self, file_settings: IFileSettings, parse_settings: IParseSettings, engine='pandas'):
        self._file_settings = file_settings
        self._parse_settings = parse_settings
        self._engine = engine

    @property
    def file_settings(self) -> IFileSettings:
        return self._file_settings

    @property
    def parse_settings(self) -> IParseSettings:
        return self._parse_settings

    @property
    def engine(self):
        return self._engine

    def read(self, usecols: Optional[List[str]] = None) -> IDataFrame:
        if self.engine == 'pandas':
            import pandas as pd
            return pd.read_csv(
                self.file_settings.file_path,
                usecols=usecols,
                sep=self.parse_settings.sep,
                skiprows=self.parse_settings.skip_rows,
                header=self.parse_settings.header,
                names=self.parse_settings.columns,
                dtype=self.parse_settings.dtypes,
                na_values=self.parse_settings.na_values,
                decimal=self.parse_settings.decimal,
                parse_dates=self.parse_settings.parse_dates,
                date_format=self.parse_settings.date_format,
                index_col=self.parse_settings.index_col,
                iterator=self.parse_settings.iterator,
                chunksize=self.parse_settings.chunksize
            )
        raise NotImplementedError
