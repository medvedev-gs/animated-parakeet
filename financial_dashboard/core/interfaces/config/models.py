import datetime as dt
from pathlib import Path
from typing import Protocol
from typing import Optional, List, Dict

from financial_dashboard.core.interfaces.filesystem import IFileSystem
from financial_dashboard.core.entities.contracts import DataSourceType, FuturesKey, DeliveryMonth


class IDataSettings(Protocol):
    source_type: DataSourceType
    futures_key: FuturesKey
    delivery_month: DeliveryMonth
    year: dt.date


class IFileSettings(Protocol):
    file_system: IFileSystem
    file_path: Path


class IParseSettings(Protocol):
    sep: str
    skip_rows: Optional[int]
    header: int
    columns: List[str]
    dtypes: Dict[str, str]
    na_values: List[str]
    datetime_cols: List[str]
    datetime_fmt: str
    decimal: str
    parse_dates: Optional[List[str]]
    date_format: Optional[str]
    index_col: Optional[str]
    iterator: bool
    chunksize: Optional[int]
