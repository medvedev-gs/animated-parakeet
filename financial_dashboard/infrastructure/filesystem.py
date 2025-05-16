from pathlib import Path
from typing import Union

from core.interfaces.filesystem import IFileSystem


class OSFileSystem(IFileSystem):
    """Реальная реализация файловой системы"""
    def exists(self, path: Path) -> bool:
        return path.exists()

    def mkdir(self, path: Path, exist_ok: bool = True) -> None:
        path.mkdir(exist_ok=exist_ok)

    def build_path(
        self,
        base_dir: Union[str, Path],
        *path_parts: Union[str, Path],
        create_dir: bool = False
    ) -> Path:
        """
        Собирает путь из частей с учётом особенностей ОС.
        
        Args:
            base_dir: Базовый каталог (например, 'data/quik')
            path_parts: Дополнительные части пути (тикер, имя файла)
            create_dir: Создать директорию, если не существует
            
        Returns:
            Path: Полный собранный путь
        """
        full_path = Path(base_dir).joinpath(*path_parts)

        if create_dir:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        return full_path
