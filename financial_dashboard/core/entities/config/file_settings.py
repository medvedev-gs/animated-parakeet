from pathlib import Path
from dataclasses import dataclass

from financial_dashboard.core.interfaces.config.models import IFileSettings


@dataclass(frozen=True)
class FileSettings(IFileSettings):
    file_path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.file_path, Path):
            raise TypeError(
                f"file_path type error: expected {Path.__name__}, got {type(self.file_path)}"
            )
