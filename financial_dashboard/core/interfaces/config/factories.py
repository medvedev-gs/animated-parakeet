from abc import ABC, abstractmethod

from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.config.models import IParseSettings


class IDataSettingsFactory(ABC):
    @abstractmethod
    @property
    def data_settings(self) -> IDataSettings:
        ...


class IParseSettingsFactory(ABC):
    @abstractmethod
    @property
    def parse_settings(self) -> IParseSettings:
        ...
