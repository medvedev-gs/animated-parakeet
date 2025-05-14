from abc import ABC, abstractmethod
from pathlib import Path

from financial_dashboard.core.interfaces.config.models import IDataSettings


class IFileName(ABC):
    def __init__(self, data_settings: IDataSettings) -> None:
        self.data_settings = data_settings

    @property
    @abstractmethod
    def file_name(self) -> Path:
        ...
