import datetime as dt
from abc import ABC, abstractmethod

from financial_dashboard.core.interfaces.config.models import IDataSettings, IFileSettings, IParseSettings
from financial_dashboard.core.interfaces.filesystem import IFileSystem
from financial_dashboard.core.entities.contracts import DataSourceType, FuturesKey, DeliveryMonth


class IDataSettingsFactory(ABC):
    @abstractmethod
    @staticmethod
    def create(
        source_type: DataSourceType,
        futures_key: FuturesKey,
        delivery_month: DeliveryMonth,
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
    def create(
        self,
        file_system: IFileSystem,
        data_settings: IDataSettings
    ) -> IFileSettings:
        pass
