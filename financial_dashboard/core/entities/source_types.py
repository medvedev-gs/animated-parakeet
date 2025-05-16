from enum import Enum


class DateTimePatterns:
    QUIK: str = '%Y%m%d %H%M%S'
    DAILY: str = '%d.%m.%Y'


class DataSourceType(str, Enum):
    """Enum representing available data source types.
    
    Attributes:
        QUIK: Data from QUIK trading system
        DAILY: Daily aggregated data
    """
    QUIK = 'quik'
    DAILY = 'daily'
