import datetime as dt
from typing import Optional, List, Dict,Protocol


class DataSourceTypeProtocol(Protocol):
    value: str


class FuturesKeyProtocol(Protocol):
    value: str


class DeliveryMonthProtocol(Protocol):
    value: str


class IDataSettings(Protocol):
    source_type: DataSourceTypeProtocol
    futures_key: FuturesKeyProtocol
    delivery_month: DeliveryMonthProtocol
    year: dt.date


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


class IParseSettingsTemplate(Protocol):
    parse_settings: IParseSettings
