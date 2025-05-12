from abc import ABC, abstractmethod

from financial_dashboard.core.interfaces.dataframe import IDataFrame


class IDataReader(ABC):
    @abstractmethod
    def read(self, usecols: list[str] = None) -> IDataFrame:
        pass
