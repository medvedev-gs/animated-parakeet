import datetime as dt
from pathlib import Path
from abc import ABC, abstractmethod

from financial_dashboard.core.interfaces.config.models import DataSourceTypeProtocol
from financial_dashboard.core.interfaces.config.models import FuturesKeyProtocol
from financial_dashboard.core.interfaces.config.models import DeliveryMonthProtocol
from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.config.models import IFileSettings
from financial_dashboard.core.interfaces.config.models import IParseSettings

from financial_dashboard.core.interfaces.filesystem import IFileSystem


class IDataSettingsFactory(ABC):
    @abstractmethod
    @staticmethod
    def create(
        source_type: DataSourceTypeProtocol,
        futures_key: FuturesKeyProtocol,
        delivery_month: DeliveryMonthProtocol,
        year: dt.date
    ) -> IDataSettings:
        pass


class IParseSettingsFactory(ABC):
    @abstractmethod
    @staticmethod
    def create(
        data_settings: IDataSettings
    ) -> IParseSettings:
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
