from pathlib import Path
from dataclasses import dataclass

from financial_dashboard.core.interfaces.config.models import IFileSettings
from financial_dashboard.core.interfaces.filesystem import IFileSystem


@dataclass(frozen=True)
class FileSettings(IFileSettings):
    file_system: IFileSystem
    file_path: Path

    def __post__init__(self) -> None:
        if not issubclass(self.file_system, IFileSystem):
            raise TypeError(
                f"file_system type error: expected {IFileSystem.__name__}, got {type(self.file_system)}"
            )
        if not isinstance(self.file_path, Path):
            raise TypeError(
                f"file_path type error: expected {Path.__name__}, got {type(self.file_path)}"
            )
        if not self.file_system.exists(self.file_path):
            raise FileNotFoundError(
                f"file_path not exists: {type(self.file_path)}"
            )
