from pathlib import Path
from abc import ABC, abstractmethod


class IFileNameGenerator(ABC):
    @abstractmethod
    @property
    def file_name(self) -> Path:
        ...


class IFileDirGenerator(ABC):
    @property
    @abstractmethod
    def file_dir(self) -> Path:
        ...


class IFilePathGenerator(ABC):
    @property
    @abstractmethod
    def file_path(self) -> Path:
        ...
