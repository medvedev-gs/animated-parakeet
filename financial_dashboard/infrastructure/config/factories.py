import datetime as dt
from pathlib import Path
from typing import Dict, Callable

from financial_dashboard.core.interfaces.config.factories import IDataSettingsFactory
from financial_dashboard.core.interfaces.config.factories import IFileSettingsFactory
from financial_dashboard.core.interfaces.config.factories import IParseSettingsFactory

from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.config.models import IFileSettings
from financial_dashboard.core.interfaces.config.models import IParseSettings

from financial_dashboard.core.interfaces.filesystem import IFileSystem

from financial_dashboard.core.entities.contracts import DataSourceType
from financial_dashboard.core.entities.contracts import FuturesKey
from financial_dashboard.core.entities.contracts import DeliveryMonth
from financial_dashboard.core.entities.contracts import ColumnNames

from financial_dashboard.core.entities.config.data_settings import DataSettings
from financial_dashboard.core.entities.config.file_settings import FileSettings
from financial_dashboard.core.entities.config.parse_settings import ParseSettings


class DataSettingsFactory(IDataSettingsFactory):
    @staticmethod
    def create(
            source_type: DataSourceType,
            futures_key: FuturesKey,
            delivery_month: DeliveryMonth,
            year: dt.date
    ) -> IDataSettings:
        """Собирает DataSettings"""
        return DataSettings(
            source_type=source_type,
            futures_key=futures_key,
            delivery_month=delivery_month,
            year=year
        )


class QuikParseSettingsMixin:
    @classmethod
    def _quik_config(cls) -> IParseSettings:
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


class DailyParseSettingsMixin:
    @classmethod
    def _daily_config(cls) -> IParseSettings:
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


class ParseSettingsFactory(IParseSettingsFactory, QuikParseSettingsMixin, DailyParseSettingsMixin):
    @staticmethod
    def create(data_settings: IDataSettings) -> IParseSettings:
        """Собирает ParseSettings из DataSettings"""
        if not isinstance(data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(data_settings)}')
        _registry: Dict[DataSourceType, Callable[[], ParseSettings]] = {
            DataSourceType.QUIK: ParseSettingsFactory._quik_config,
            DataSourceType.DAILY: ParseSettingsFactory._daily_config,
        }
        if not data_settings.source_type in _registry:
            raise ValueError(f'unregistered source_type {data_settings.source_type.value}')
        return _registry[data_settings.source_type]()


class QuikFileNameMixin:
    @classmethod
    def _quik_file_name(cls, data_settings: IDataSettings) -> Path:
        return Path(
            f'{data_settings.futures_key.value}{data_settings.delivery_month.value}{data_settings.year.strftime('%Y')[-1]}.csv'
        )


class DailyFileNameMixin:
    @classmethod
    def _daily_file_name(cls, data_settings: IDataSettings) -> Path:
        return Path(
            f'{data_settings.futures_key.value}{data_settings.delivery_month.value}{data_settings.year.strftime('%Y')[-2:]}.csv'
        )


class FileNameFactory(QuikFileNameMixin, DailyFileNameMixin):
    @staticmethod
    def create(data_settings: IDataSettings) -> Path:
        if not isinstance(data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(data_settings)}')
        _registry: Dict[DataSourceType, Callable[[IDataSettings], Path]] = {
            DataSourceType.QUIK: FileNameFactory._quik_file_name,
            DataSourceType.DAILY: FileNameFactory._daily_file_name,
        }
        if not data_settings.source_type in _registry:
            raise ValueError(f'unregistered source_type: {data_settings.source_type.value}')
        return _registry[data_settings.source_type](data_settings)


class FileDirFactory:
    @staticmethod
    def create(
        file_system: IFileSystem,
        root_path: Path,
        data_settings: IDataSettings
    ) -> Path:
        if not issubclass(file_system, IFileSystem):
            raise TypeError(f'file_system type error: expected {IFileSystem.__name__}, got {type(file_system)}')
        if not isinstance(root_path, Path):
            raise TypeError(f'root_path type error: expected {Path.__name__}, got {type(root_path)}')
        if not isinstance(data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(data_settings)}')
        _registry: Dict[DataSourceType, Path] = {
            DataSourceType.DAILY: Path('data/daily_data'),
            DataSourceType.QUIK: Path('data/quik_data'),
        }
        if not data_settings.source_type in _registry:
            raise ValueError(f'unregistered source_type: {data_settings.source_type.value}')
        return file_system.build_path(
            root_path,
            _registry[data_settings.source_type],
            data_settings.futures_key.value
        )


class FileSettingsFactory(IFileSettingsFactory):
    @staticmethod
    def create(
            data_dir: Path,
            file_name: Path,
            file_system: IFileSystem
    ) -> IFileSettings:
        """Собирает FilePath из DataSettings"""
        if not isinstance(data_dir, Path):
            raise TypeError(f'data_dir type error: expected {Path.__name__}, got {type(data_dir)}')
        if not isinstance(file_name, Path):
            raise TypeError(f'file_name type error: expected {Path.__name__}, got {type(file_name)}')
        if not issubclass(file_system, IFileSystem):
            raise TypeError(f'file_system type error: expected {IFileSystem.__name__}, got {type(file_system)}')
        file_path = file_system.build_path(data_dir, file_name)
        if not file_system.exists(file_path):
            raise FileNotFoundError(
                f"file_path not exists: {type(file_path)}"
            )
        return FileSettings(file_path=file_path)
