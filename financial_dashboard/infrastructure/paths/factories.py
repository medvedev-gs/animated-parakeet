from pathlib import Path
from typing import Dict, Type

from financial_dashboard.core.entities.contracts import DataSourceType
from financial_dashboard.core.interfaces.config.models import IDataSettings
from financial_dashboard.core.interfaces.paths.models import IFileName
from financial_dashboard.core.interfaces.filesystem import IFileSystem


class FileNameFactory:
    _registry: Dict[DataSourceType, Type[IFileName]] = {}

    def __init__(self, data_settings: IDataSettings) -> None:
        self.data_settings = data_settings

    @classmethod
    def register(cls, source_type: DataSourceType):
        def wrapper(subclass: Type[IFileName]):
            cls._registry[source_type] = subclass
            return subclass
        return wrapper

    @property
    def file_name(self) -> Path:
        if not isinstance(self.data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(self.data_settings)}')
        if not self.data_settings.source_type in FileNameFactory._registry:
            raise ValueError(f'unregistered source_type: {self.data_settings.source_type.value}')
        return FileNameFactory._registry[self.data_settings.source_type](data_settings=self.data_settings)._file_name


@FileNameFactory.register(DataSourceType.QUIK)
class QuikFileName(IFileName):
    @property
    def file_name(self) -> Path:
        return Path(
            f'{self.data_settings.futures_key.value}{self.data_settings.delivery_month.value}{self.data_settings.year.strftime('%Y')[-1]}.csv'
        )


@FileNameFactory.register(DataSourceType.DAILY)
class DailyFileName(IFileName):
    @property
    def file_name(self) -> Path:
        return Path(
            f'{self.data_settings.futures_key.value}{self.data_settings.delivery_month.value}{self.data_settings.year.strftime('%Y')[-2:]}.csv'
        )


class FileDirFactory:
    _registry: Dict[DataSourceType, Path] = {
        DataSourceType.DAILY: Path('data/daily_data'),
        DataSourceType.QUIK: Path('data/quik_data'),
    }

    def __init__(
            self,
            file_system: IFileSystem,
            root_path: Path,
            data_settings: IDataSettings
    ) -> None:
        self.file_system = file_system
        self.root_path = root_path
        self.data_settings = data_settings

    @property
    def file_dir(self) -> Path:
        if not issubclass(self.file_system, IFileSystem):
            raise TypeError(f'file_system type error: expected {IFileSystem.__name__}, got {type(self.file_system)}')
        if not isinstance(self.root_path, Path):
            raise TypeError(f'root_path type error: expected {Path.__name__}, got {type(self.root_path)}')
        if not isinstance(self.data_settings, IDataSettings):
            raise TypeError(f'data_settings type error: expected {IDataSettings.__name__}, got {type(self.data_settings)}')
        if not self.data_settings.source_type in FileDirFactory._registry:
            raise ValueError(f'unregistered source_type: {self.data_settings.source_type.value}')
        return self.file_system.build_path(
            self.root_path,
            FileDirFactory._registry[self.data_settings.source_type],
            self.data_settings.futures_key.value
        )
