import datetime as dt
from pathlib import Path
from typing import Dict, Type, Any
from enum import Enum

from financial_dashboard.core.interfaces.config.factories import IDataSettingsFactory
from financial_dashboard.core.interfaces.config.factories import IParseSettingsFactory
from financial_dashboard.core.interfaces.config.factories import IFileSettingsFactory

from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.config.models import IParseSettings
from financial_dashboard.core.interfaces.config.models import ISourceTypeParseSettings
from financial_dashboard.core.interfaces.config.models import IFileSettings
from financial_dashboard.core.interfaces.config.models import IFileName

from financial_dashboard.core.interfaces.filesystem import IFileSystem

from financial_dashboard.core.entities.contracts import DataSourceType
from financial_dashboard.core.entities.contracts import FuturesKey
from financial_dashboard.core.entities.contracts import DeliveryMonth
from financial_dashboard.core.entities.contracts import ColumnNames

from financial_dashboard.core.entities.config.data_settings import DataSettings
from financial_dashboard.core.entities.config.parse_settings import ParseSettings
from financial_dashboard.core.entities.config.file_settings import FileSettings


class EnumValidatorMixin:
    """Миксин для автоматической валидации enum'ов при присвоении атрибутов."""
    _enum_types: Dict[str, Type[Enum]] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._enum_types and not isinstance(value, self._enum_types[name]):
            raise TypeError(
                f"Поле {name} должно быть типом {self._enum_types[name].__name__}, получено: {type(value)}"
            )
        super().__setattr__(name, value)


class DataSettingsFactory(IDataSettingsFactory, EnumValidatorMixin):
    "Data Configuration Factory"
    _enum_types: Dict[str, Type[Enum]] = {
        "source_type": DataSourceType,
        "futures_key": FuturesKey,
        "delivery_month": DeliveryMonth,
    }

    @property
    def data_settings(self) -> IDataSettings:
        """Creates DataSettings"""
        return DataSettings(
            source_type=self.source_type,
            futures_key=self.futures_key,
            delivery_month=self.delivery_month,
            year=self.year
        )


class QuikParseSettings(ISourceTypeParseSettings):
    @property
    def _parse_settings(self) -> IParseSettings:
        return ParseSettings(
            sep=',',
            skip_rows=None,
            header=0,
            columns=[
                ColumnNames.TICKER,
                ColumnNames.PER,
                ColumnNames.DATE,
                ColumnNames.TIME,
                ColumnNames.OPEN,
                ColumnNames.HIGH,
                ColumnNames.LOW,
                ColumnNames.CLOSE,
                ColumnNames.VOL
            ],
            dtypes={
                ColumnNames.TICKER: 'category',
                ColumnNames.PER: 'Int64',
                ColumnNames.DATE: 'string',
                ColumnNames.TIME: 'string',
                ColumnNames.OPEN: 'float64',
                ColumnNames.HIGH: 'float64',
                ColumnNames.LOW: 'float64',
                ColumnNames.CLOSE: 'float64',
                ColumnNames.VOL: 'Int64'
            },
            na_values=[''],
            datetime_cols=[ColumnNames.DATE, ColumnNames.TIME],
            datetime_fmt='%Y%m%d %H%M%S',
            decimal='.',
            parse_dates=None,
            date_format=None,
            index_col=None,
            iterator=False,
            chunksize=None
        )


class DailyParseSettings(ISourceTypeParseSettings):
    @property
    def _parse_settings(self) -> IParseSettings:
        return ParseSettings(
            sep=',',
            skip_rows=2,
            header=0,
            columns=[
                ColumnNames.BOARDID,
                ColumnNames.DATE,
                ColumnNames.TICKER,
                ColumnNames.OPEN,
                ColumnNames.LOW,
                ColumnNames.HIGH,
                ColumnNames.CLOSE,
                ColumnNames.OPENPOSITIONVALUE,
                ColumnNames.VALUE,
                ColumnNames.VOL,
                ColumnNames.OPENPOSITION,
                ColumnNames.SETTLEPRICE,
                ColumnNames.WAPRICE,
                ColumnNames.SETTLEPRICEDAY,
                ColumnNames.CHANGE,
                ColumnNames.QTY,
                ColumnNames.NUMTRADES
            ],
            dtypes={
                ColumnNames.BOARDID: 'category',
                ColumnNames.DATE: 'string',
                ColumnNames.TICKER: 'category',
                ColumnNames.OPEN: 'float64',
                ColumnNames.LOW: 'float64',
                ColumnNames.HIGH: 'float64',
                ColumnNames.CLOSE: 'float64',
                ColumnNames.OPENPOSITIONVALUE: 'float64',
                ColumnNames.VALUE: 'float64',
                ColumnNames.VOL: 'Int64',
                ColumnNames.OPENPOSITION: 'Int64',
                ColumnNames.SETTLEPRICE: 'float64',
                ColumnNames.WAPRICE: 'float64',
                ColumnNames.SETTLEPRICEDAY: 'float64',
                ColumnNames.CHANGE: 'float64',
                ColumnNames.QTY: 'Int64',
                ColumnNames.NUMTRADES: 'Int64'
            },
            na_values=[''],
            datetime_cols=[ColumnNames.DATE],
            datetime_fmt='%d.%m.%Y',
            decimal='.',
            parse_dates=None,
            date_format=None,
            index_col=None,
            iterator=False,
            chunksize=None
        )


class ParseSettingsFactory(IParseSettingsFactory):
    _registry: Dict[DataSourceType, Type[ISourceTypeParseSettings]] = {
        DataSourceType.QUIK: QuikParseSettings,
        DataSourceType.DAILY: DailyParseSettings,
    }

    def __init__(self, data_settings: IDataSettings) -> None:
        self.data_settings = data_settings

    @property
    def parse_settings(self) -> IParseSettings:
        """Собирает ParseSettings из DataSettings"""
        if not isinstance(self.data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(self.data_settings)}')
        if not self.data_settings.source_type in ParseSettingsFactory._registry:
            raise ValueError(f'unregistered source_type {self.data_settings.source_type.value}')
        return ParseSettingsFactory._registry[self.data_settings.source_type]._parse_settings


class QuikFileName(IFileName):
    @property
    def _file_name(self) -> Path:
        return Path(
            f'{self.data_settings.futures_key.value}{self.data_settings.delivery_month.value}{self.data_settings.year.strftime('%Y')[-1]}.csv'
        )


class DailyFileName(IFileName):
    @property
    def _file_name(self) -> Path:
        return Path(
            f'{self.data_settings.futures_key.value}{self.data_settings.delivery_month.value}{self.data_settings.year.strftime('%Y')[-2:]}.csv'
        )


class FileNameFactory:
    _registry: Dict[DataSourceType, Type[IFileName]] = {
        DataSourceType.QUIK: QuikFileName,
        DataSourceType.DAILY: DailyFileName,
    }

    def __init__(self, data_settings: IDataSettings) -> None:
        self.data_settings = data_settings

    @property
    def file_name(self) -> Path:
        if not isinstance(self.data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(self.data_settings)}')
        if not self.data_settings.source_type in FileNameFactory._registry:
            raise ValueError(f'unregistered source_type: {self.data_settings.source_type.value}')
        return FileNameFactory._registry[self.data_settings.source_type](data_settings=self.data_settings)._file_name


class FileDirFactory:
    _registry: Dict[DataSourceType, Path] = {
        DataSourceType.DAILY: Path('data/daily_data'),
        DataSourceType.QUIK: Path('data/quik_data'),
    }

    def __init__(
            self,
            file_system: IFileSystem,
            root_path: Path,
            data_settings: IDataSettings
    ) -> None:
        self.file_system = file_system
        self.root_path = root_path
        self.data_settings = data_settings

    @property
    def file_dir(self) -> Path:
        if not issubclass(self.file_system, IFileSystem):
            raise TypeError(f'file_system type error: expected {IFileSystem.__name__}, got {type(self.file_system)}')
        if not isinstance(self.root_path, Path):
            raise TypeError(f'root_path type error: expected {Path.__name__}, got {type(self.root_path)}')
        if not isinstance(self.data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(self.data_settings)}')
        if not self.data_settings.source_type in FileDirFactory._registry:
            raise ValueError(f'unregistered source_type: {self.data_settings.source_type.value}')
        return self.file_system.build_path(
            self.root_path,
            FileDirFactory._registry[self.data_settings.source_type],
            self.data_settings.futures_key.value
        )


class FileSettingsFactory(IFileSettingsFactory):
    def __init__(
            self,
            data_dir_factory: FileDirFactory,
            file_name_factory: FileNameFactory,
            file_system: IFileSystem
    ) -> None:
        self.data_dir_factory = data_dir_factory
        self.file_name_factory = file_name_factory
        self.file_system = file_system

    @property
    def create(self) -> IFileSettings:
        """Собирает FilePath из DataSettings"""
        if not isinstance(self.data_dir_factory, FileDirFactory):
            raise TypeError(f'data_dir type error: expected {FileDirFactory.__name__}, got {type(self.data_dir_factory)}')
        if not isinstance(self.file_name_factory, FileNameFactory):
            raise TypeError(f'file_name type error: expected {FileNameFactory.__name__}, got {type(self.file_name_factory)}')
        if not issubclass(self.file_system, IFileSystem):
            raise TypeError(f'file_system type error: expected {IFileSystem.__name__}, got {type(self.file_system)}')
        file_path = self.file_system.build_path(self.data_dir_factory.file_dir, self.file_name_factory.file_name)
        if not self.file_system.exists(file_path):
            raise FileNotFoundError(
                f"file_path not exists: {type(file_path)}"
            )
        return FileSettings(file_path=file_path)
