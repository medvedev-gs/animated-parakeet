from abc import ABC, abstractmethod

from financial_dashboard.core.interfaces.paths.models import IFileNameGenerator
from financial_dashboard.core.interfaces.paths.models import IFileDirGenerator
from financial_dashboard.core.interfaces.paths.models import IFilePathGenerator


class IFileNameGeneratorFactory(ABC):
    @abstractmethod
    @property
    def file_name_generator(self) -> IFileNameGenerator:
        ...


class IFileDirGeneratorFactory(ABC):
    @abstractmethod
    @property
    def file_dir_generator(self) -> IFileDirGenerator:
        ...


class IFilePathGeneratorFactory(ABC):
    @abstractmethod
    @property
    def file_path_generator(self) -> IFilePathGenerator:
        ...
