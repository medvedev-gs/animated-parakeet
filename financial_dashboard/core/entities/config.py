import datetime as dt
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict

from financial_dashboard.core.interfaces.config.models import IParseSettings

from financial_dashboard.core.interfaces.config.models import DataSourceTypeProtocol
from financial_dashboard.core.interfaces.config.models import FuturesKeyProtocol
from financial_dashboard.core.interfaces.config.models import DeliveryMonthProtocol
from financial_dashboard.core.interfaces.config.models import IDataSettings


class DataSettings(BaseModel, IDataSettings):
    model_config = ConfigDict(frozen=True)

    source_type: DataSourceTypeProtocol
    futures_key: FuturesKeyProtocol
    delivery_month: DeliveryMonthProtocol
    year: dt.date


class ParseSettings(BaseModel, IParseSettings):
    model_config = ConfigDict(frozen=True)

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
