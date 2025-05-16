from pathlib import Path
from typing import Dict, Type, Optional, Callable

from financial_dashboard.core.interfaces.config.models import DataSourceTypeProtocol
from financial_dashboard.core.interfaces.config.models import IDataSettings

from financial_dashboard.core.interfaces.config.factories import IDataSettingsFactory

from financial_dashboard.core.interfaces.paths.models import IFileNameGenerator
from financial_dashboard.core.interfaces.paths.models import IFileDirGenerator
from financial_dashboard.core.interfaces.paths.models import IFilePathGenerator

from financial_dashboard.core.interfaces.paths.factories import IFileNameGeneratorFactory
from financial_dashboard.core.interfaces.paths.factories import IFileDirGeneratorFactory
from financial_dashboard.core.interfaces.paths.factories import IFilePathGeneratorFactory

from financial_dashboard.core.interfaces.filesystem import IFileSystem

from financial_dashboard.core.entities.source_types import DataSourceType


class FileNameGeneratorFactory(IFileNameGeneratorFactory):
    _registry: Dict[DataSourceTypeProtocol, Type[IFileNameGenerator]] = {}

    def __init__(self, data_settings_factory: IDataSettingsFactory) -> None:
        self._data_settings_factory = data_settings_factory
        self._file_name_generator_cache: Optional[IFileNameGenerator] = None

    def clear_cache(self) -> None:
        self._file_name_generator_cache = None

    @property
    def _data_settings(self) -> IDataSettings:
        return self._data_settings_factory.data_settings

    @classmethod
    def _register(cls, source_type: DataSourceTypeProtocol) -> Callable[[Type[IFileNameGenerator], Type[IFileNameGenerator]]]:
        def wrapper(file_name_class: Type[IFileNameGenerator]) -> Type[IFileNameGenerator]:
            cls._registry[source_type] = file_name_class
            return file_name_class
        return wrapper

    def _load_cache(self) -> IFileNameGenerator:
        if not isinstance(self._data_settings_factory, IDataSettingsFactory):
            raise TypeError(f'data_settings_factory type error: expected {IDataSettingsFactory.__name__}, got {type(self._data_settings_factory)}')
        if not self._data_settings.source_type in FileNameGeneratorFactory._registry:
            raise ValueError(f'unregistered source_type: {self._data_settings.source_type.value}')
        return FileNameGeneratorFactory._registry[self._data_settings.source_type](data_settings=self._data_settings)

    @property
    def file_name_generator(self) -> IFileNameGenerator:
        if self._file_name_generator_cache is None:
            self._file_name_generator_cache = self._load_cache()
        return self._file_name_generator_cache


@FileNameGeneratorFactory._register(DataSourceType.QUIK)
class QuikFileNameGenerator(IFileNameGenerator):

    def __init__(self, data_settings: IDataSettings) -> None:
        self._data_settings = data_settings
        self._file_name_cache: Optional[Path] = Path

    def clear_cache(self) -> None:
        self._file_name_cache = None

    @property
    def file_name(self) -> Path:
        if self._file_name_cache is None:
            self._file_name_cache = Path(
                f'{self._data_settings.futures_key.value}'
                f'{self._data_settings.delivery_month.value}'
                f'{self._data_settings.year.strftime('%Y')[-1]}.csv'
            )
        return self._file_name_cache


@FileNameGeneratorFactory._register(DataSourceType.DAILY)
class DailyFileNameGenerator(IFileNameGenerator):

    def __init__(self, data_settings: IDataSettings) -> None:
        self._data_settings = data_settings
        self._file_name_cache: Optional[Path] = Path

    def clear_cache(self) -> None:
        self._file_name_cache = None

    @property
    def file_name(self) -> Path:
        if self._file_name_cache is None:
            self._file_name_cache = Path(
                f'{self._data_settings.futures_key.value}'
                f'{self._data_settings.delivery_month.value}'
                f'{self._data_settings.year.strftime('%Y')[-2:]}.csv'
            )
        return self._file_name_cache


class FileDirGeneratorFactory(IFileDirGeneratorFactory):
    _registry: Dict[DataSourceType, Type[IFileDirGenerator]] = {}

    def __init__(
            self,
            file_system: IFileSystem,
            root_path: Path,
            data_settings_factory: IDataSettingsFactory
    ) -> None:
        self._file_system = file_system
        self._root_path = root_path
        self._data_settings_factory = data_settings_factory
        self._file_dir_generator_cache: Optional[IFileDirGenerator] = None

    def clear_cache(self) -> None:
        self._file_dir_generator_cache = None

    @property
    def _data_settings(self) -> IDataSettings:
        return self._data_settings_factory.data_settings

    def _load_cache(self) -> IFileDirGenerator:
        if not issubclass(self._file_system, IFileSystem):
            raise TypeError(f'file_system type error: expected {IFileSystem.__name__}, got {type(self._file_system)}')
        if not isinstance(self._root_path, Path):
            raise TypeError(f'root_path type error: expected {Path.__name__}, got {type(self._root_path)}')
        if not isinstance(self._data_settings_factory, IDataSettingsFactory):
            raise TypeError(f'_data_settings_factory type error: expected {IDataSettingsFactory.__name__}, got {type(self._data_settings_factory)}')
        if not self._data_settings.source_type in FileDirGeneratorFactory._registry:
            raise ValueError(f'unregistered source_type: {self._data_settings.source_type.value}')
        return  FileDirGeneratorFactory._registry[self._data_settings.source_type]()

    @classmethod
    def _register(cls, source_type: DataSourceTypeProtocol) -> Callable[[Type[IFileDirGenerator], Type[IFileDirGenerator]]]:
        def wrapper(file_dir_class: Type[IFileDirGenerator]) -> Type[IFileDirGenerator]:
            cls._registry[source_type] = file_dir_class
            return file_dir_class
        return wrapper

    @property
    def file_dir_generator(self) -> IFileDirGenerator:
        if self._file_dir_generator_cache is None:
            self._file_dir_generator_cache = self._load_cache()
        return self._file_dir_generator_cache


@FileDirGeneratorFactory._register(DataSourceType.QUIK)
class QuikFileDirGenerator(IFileDirGenerator):

    def __init__(self, file_system: IFileSystem, root_path: Path, data_settings: IDataSettings) -> None:
        self._fs = file_system
        self._root = root_path
        self._data_settings = data_settings
        self._file_dir_cache = Optional[Path] = None

    def clear_cache(self) -> None:
        self._file_dir_cache = None

    @property
    def _data_dir(self):
        return Path('data/quik_data')

    def _load_cache(self) -> Path:
        return self._fs.build_path(self._root, self._data_dir, self._data_settings.futures_key.value)

    @property
    def file_dir(self) -> Path:
        if self._file_dir_cache is None:
            self._file_dir_cache = self._load_cache()
        return self._file_dir_cache


@FileDirGeneratorFactory._register(DataSourceType.DAILY)
class DailyFileDirGenerator(IFileDirGenerator):

    def __init__(self, file_system: IFileSystem, root_path: Path, data_settings: IDataSettings) -> None:
        self._fs = file_system
        self._root = root_path
        self._data_settings = data_settings
        self._file_dir_cache = Optional[Path] = None

    def clear_cache(self) -> None:
        self._file_dir_cache = None

    @property
    def _data_dir(self):
        return Path('data/daily_data')

    def _load_cache(self) -> Path:
        return self._fs.build_path(self._root, self._data_dir, self._data_settings.futures_key.value)

    @property
    def file_dir(self) -> Path:
        if self._file_dir_cache is None:
            self._file_dir_cache = self._load_cache()
        return self._file_dir_cache


class FilePathGenerator(IFilePathGenerator):
    def __init__(self, file_system: IFileSystem, file_dir_generator: IFileDirGenerator, file_name_generator: IFileNameGenerator):
        self._fs = file_system
        self._file_dir_generator = file_dir_generator
        self._file_name_generator = file_name_generator
        self._file_path_cache = Optional[Path]

    def _load_cache(self) -> Path:
        file_path = self._fs.build_path(self._file_dir_generator.file_dir, self._file_name_generator.file_name)
        if not self._fs.exists(file_path):
            raise FileNotFoundError(
                f"file_path not exists: {type(file_path)}"
            )
        return file_path

    def clear_cache(self) -> None:
        self._file_path_cache = None

    @property
    def file_path(self) -> Path:
        if self._file_path_cache is None:
            self._file_path_cache = self._load_cache()
        return self._file_path_cache


class FilePathGeneratorFactory(IFilePathGeneratorFactory):
    def __init__(
            self,
            file_dir_factory: IFileDirGeneratorFactory,
            file_name_factory: IFileNameGeneratorFactory,
            file_system: IFileSystem
    ) -> None:
        self._data_dir_factory = file_dir_factory
        self._file_name_factory = file_name_factory
        self._file_system = file_system
        self._file_path_generator_cache: Optional[IFilePathGenerator] = None

    def _load_cache(self) -> IFilePathGenerator:
        if not isinstance(self._data_dir_factory, IFileDirGeneratorFactory):
            raise TypeError(f'data_dir type error: expected {IFileDirGeneratorFactory.__name__}, got {type(self._data_dir_factory)}')
        if not isinstance(self._file_name_factory, IFileNameGeneratorFactory):
            raise TypeError(f'file_name type error: expected {IFileNameGeneratorFactory.__name__}, got {type(self._file_name_factory)}')
        if not issubclass(self._file_system, IFileSystem):
            raise TypeError(f'file_system type error: expected {IFileSystem.__name__}, got {type(self._file_system)}')
        return FilePathGenerator(fs=self._file_system, file_dir_generator=self._data_dir_factory.file_dir_generator, file_name_generator=self._file_name_factory.file_name_generator)

    def clear_cache(self) -> None:
        self._file_path_generator_cache = None

    @property
    def file_path_generator(self) -> IFilePathGenerator:
        """Собирает FilePath из DataSettings"""
        if self._file_path_generator_cache is None:
            self._file_path_generator_cache = self._load_cache()
        return self._file_path_generator_cache
