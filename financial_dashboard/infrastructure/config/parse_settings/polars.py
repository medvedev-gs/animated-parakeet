from typing import Dict, Type, Callable, Optional

from financial_dashboard.core.entities.errors import *

from financial_dashboard.core.interfaces.config.factories import IDataSettingsFactory
from financial_dashboard.core.interfaces.config.factories import IParseSettingsFactory

from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.config.models import IParseSettingsTemplate
from financial_dashboard.core.interfaces.config.models import IParseSettings

from financial_dashboard.core.interfaces.config.models import DataSourceTypeProtocol

from financial_dashboard.core.entities.source_types import DateTimePatterns
from financial_dashboard.core.entities.source_types import DataSourceType
from financial_dashboard.core.entities.columns import ColumnNames
from financial_dashboard.core.entities.columns import DTypes
from financial_dashboard.core.entities.columns import Separators

from financial_dashboard.core.entities.config import ParseSettings


class ParseSettingsFactory(IParseSettingsFactory):
    _registry: Dict[DataSourceTypeProtocol, Type[IParseSettingsTemplate]] = {}

    def __init__(self, data_settings_factory: IDataSettingsFactory) -> None:
        self._data_settings_factory = data_settings_factory
        self._parse_settings_cache: Optional[IParseSettings] = None

    @property
    def _data_settings(self) -> IDataSettings:
        return self._data_settings_factory.data_settings

    @classmethod
    def _register(cls, source_type: DataSourceTypeProtocol) -> Callable[[Type[IParseSettingsTemplate]], Type[IParseSettingsTemplate]]:
        if not isinstance(source_type, DataSourceTypeProtocol):
            raise DataSourceTypeError(f'source_type type error: expected {DataSourceTypeProtocol.__name__}, got {type(source_type)}')
        def wrapper(settings_class: Type[IParseSettingsTemplate]) -> Type[IParseSettingsTemplate]:
            if not issubclass(settings_class, IParseSettingsTemplate):
                raise IParseSettingsTemplateError(f'subclass type error: expected {IParseSettingsTemplate.__name__},  got {type(settings_class)}')
            cls._registry[source_type] = settings_class
            return settings_class
        return wrapper

    @classmethod
    def register_custom_source(
        cls,
        source_type: DataSourceTypeProtocol,
        settings_class: Type[IParseSettingsTemplate]
    ) -> None:
        """Register a custom data source type with its parse settings."""
        if not isinstance(source_type, DataSourceTypeProtocol):
            raise DataSourceTypeError(f'source_type type error: expected {DataSourceTypeProtocol.__name__}, got {type(source_type)}')
        if not issubclass(settings_class, IParseSettingsTemplate):
            raise IParseSettingsTemplateError(f'subclass type error: expected {IParseSettingsTemplate.__name__},  got {type(settings_class)}')
        cls._registry[source_type] = settings_class

    @property
    def parse_settings(self) -> IParseSettings:
        """Собирает ParseSettings из DataSettings"""
        if self._parse_settings_cache is None:
            if not self._data_settings.source_type in ParseSettingsFactory._registry:
                raise UnregisteredSourceTypeError(f'unregistered source_type {self._data_settings.source_type.value}')
            self._parse_settings_cache = ParseSettingsFactory._registry[self._data_settings.source_type]().parse_settings
        return self._parse_settings_cache


@ParseSettingsFactory._register(DataSourceType.QUIK)
class QuikParseSettings(IParseSettingsTemplate):
    @property
    def parse_settings(self) -> IParseSettings:
        return ParseSettings(
            sep=Separators.COMMA,
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
            datetime_fmt=DateTimePatterns.QUIK,
            decimal=Separators.DOT,
            parse_dates=None,
            date_format=None,
            index_col=None,
            iterator=False,
            chunksize=None
        )


@ParseSettingsFactory._register(DataSourceType.DAILY)
class DailyParseSettings(IParseSettingsTemplate):
    @property
    def parse_settings(self) -> IParseSettings:
        return ParseSettings(
            sep=Separators.COMMA,
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
                ColumnNames.BOARDID: DTypes.CATEGORY,
                ColumnNames.DATE: DTypes.STRING,
                ColumnNames.TICKER: DTypes.CATEGORY,
                ColumnNames.OPEN: DTypes.FLOAT64,
                ColumnNames.LOW: DTypes.FLOAT64,
                ColumnNames.HIGH: DTypes.FLOAT64,
                ColumnNames.CLOSE: DTypes.FLOAT64,
                ColumnNames.OPENPOSITIONVALUE: DTypes.FLOAT64,
                ColumnNames.VALUE: DTypes.FLOAT64,
                ColumnNames.VOL: DTypes.INT64,
                ColumnNames.OPENPOSITION: DTypes.INT64,
                ColumnNames.SETTLEPRICE: DTypes.FLOAT64,
                ColumnNames.WAPRICE: DTypes.FLOAT64,
                ColumnNames.SETTLEPRICEDAY: DTypes.FLOAT64,
                ColumnNames.CHANGE: DTypes.FLOAT64,
                ColumnNames.QTY: DTypes.INT64,
                ColumnNames.NUMTRADES: DTypes.INT64
            },
            na_values=[''],
            datetime_cols=[ColumnNames.DATE],
            datetime_fmt=DateTimePatterns.DAILY,
            decimal=Separators.DOT,
            parse_dates=None,
            date_format=None,
            index_col=None,
            iterator=False,
            chunksize=None
        )
