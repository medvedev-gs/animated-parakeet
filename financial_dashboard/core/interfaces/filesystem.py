from abc import ABC, abstractmethod
from pathlib import Path


class IFileSystem(ABC):
    @abstractmethod
    def exists(self, path: Path) -> bool:
        ...

    @abstractmethod
    def mkdir(self, path: Path, exist_ok: bool = True) -> None:
        ...

    @abstractmethod
    def build_path(self, *args, **kwargs) -> Path:
        ...
