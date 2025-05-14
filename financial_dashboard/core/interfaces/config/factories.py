import datetime as dt
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional

from financial_dashboard.core.interfaces.config.models import DataSourceTypeProtocol
from financial_dashboard.core.interfaces.config.models import FuturesKeyProtocol
from financial_dashboard.core.interfaces.config.models import DeliveryMonthProtocol
from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.config.models import IParseSettings
from financial_dashboard.core.interfaces.config.models import IFileSettings

from financial_dashboard.core.interfaces.filesystem import IFileSystem


class IDataSettingsFactory(ABC):
    def __init__(
            self,
            source_type: DataSourceTypeProtocol,
            futures_key: FuturesKeyProtocol,
            delivery_month: DeliveryMonthProtocol,
            year: dt.date
    ) -> None:
        self.source_type = source_type
        self.futures_key = futures_key
        self.delivery_month = delivery_month
        self.year = year
        # Cache:
        self._data_settings_cache: Optional[IDataSettings] = None

    def clear_cache(self) -> None:
        self._data_settings_cache = None

    @abstractmethod
    @property
    def data_settings(self) -> IDataSettings:
        pass


class IParseSettingsFactory(ABC):
    def __init__(self, data_settings_factory: IDataSettingsFactory) -> None:
        self.data_settings_factory = data_settings_factory

    @property
    def data_settings(self) -> IDataSettings:
        return self.data_settings_factory.data_settings

    @abstractmethod
    @property
    def parse_settings(self) -> IParseSettings:
        pass


class IFileSettingsFactory(ABC):
    @abstractmethod
    @staticmethod
    def create(
        data_dir: Path,
        file_name: Path,
        file_system: IFileSystem
    ) -> IFileSettings:
        pass
