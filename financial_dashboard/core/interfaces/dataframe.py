from abc import ABC, abstractmethod


class IDataFrame(ABC):
    @abstractmethod
    def filter_rows(self, condition) -> 'IDataFrame': ...
    
    @abstractmethod
    def select_cols(self, columns: list[str]) -> 'IDataFrame': ...
