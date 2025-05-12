from typing import Optional, List, Dict
from dataclasses import dataclass

from financial_dashboard.core.interfaces.config.models import IParseSettings


@dataclass(frozen=True)
class ParseSettings(IParseSettings):
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
