from typing import Dict, Type, Any, Callable
from enum import Enum

from financial_dashboard.core.interfaces.config.factories import IDataSettingsFactory
from financial_dashboard.core.interfaces.config.factories import IParseSettingsFactory
from financial_dashboard.core.interfaces.config.factories import IFileSettingsFactory

from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.config.models import IParseSettingsTemplate
from financial_dashboard.core.interfaces.config.models import IParseSettings
from financial_dashboard.core.interfaces.config.models import IFileSettings

from financial_dashboard.core.interfaces.filesystem import IFileSystem

from financial_dashboard.core.entities.contracts import DataSourceType
from financial_dashboard.core.entities.contracts import FuturesKey
from financial_dashboard.core.entities.contracts import DeliveryMonth
from financial_dashboard.core.entities.contracts import ColumnNames
from financial_dashboard.core.entities.contracts import DTypes

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
        if self._data_settings_cache is None:
            self._data_settings_cache = DataSettings(
                source_type=self.source_type,
                futures_key=self.futures_key,
                delivery_month=self.delivery_month,
                year=self.year
            )
        return self._data_settings_cache


class ParseSettingsFactory(IParseSettingsFactory):
    _registry: Dict[DataSourceType, Type[IParseSettingsTemplate]] = {}

    @classmethod
    def register(cls, source_type: DataSourceType) -> Callable[[Type[IParseSettingsTemplate]], Type[IParseSettingsTemplate]]:
        if not isinstance(source_type, DataSourceType):
            raise TypeError(f'source_type type error: expected {DataSourceType.__name__}, got {type(source_type)}')
        def wrapper(subclass: Type[IParseSettingsTemplate]) -> Type[IParseSettingsTemplate]:
            if not issubclass(subclass, IParseSettingsTemplate):
                raise TypeError(f'subclass type error: expected {IParseSettingsTemplate.__name__},  got {type(subclass)}')
            cls._registry[source_type] = subclass
            return subclass
        return wrapper

    @property
    def parse_settings(self) -> IParseSettings:
        """Собирает ParseSettings из DataSettings"""
        if not self.data_settings.source_type in ParseSettingsFactory._registry:
            raise ValueError(f'unregistered source_type {self.data_settings.source_type.value}')
        return ParseSettingsFactory._registry[self.data_settings.source_type].parse_settings


@ParseSettingsFactory.register(DataSourceType.QUIK)
class QuikParseSettings(IParseSettingsTemplate):
    @property
    def parse_settings(self) -> IParseSettings:
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
                ColumnNames.TICKER: DTypes.CATEGORY,
                ColumnNames.PER: DTypes.INT64,
                ColumnNames.DATE: DTypes.STRING,
                ColumnNames.TIME: DTypes.STRING,
                ColumnNames.OPEN: DTypes.FLOAT64,
                ColumnNames.HIGH: DTypes.FLOAT64,
                ColumnNames.LOW: DTypes.FLOAT64,
                ColumnNames.CLOSE: DTypes.FLOAT64,
                ColumnNames.VOL: DTypes.INT64
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


@ParseSettingsFactory.register(DataSourceType.QUIK)
class DailyParseSettings(IParseSettingsTemplate):
    @property
    def parse_settings(self) -> IParseSettings:
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
