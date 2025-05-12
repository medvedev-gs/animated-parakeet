import datetime as dt
from pydantic import BaseModel, ConfigDict, field_validator

from financial_dashboard.core.entities.contracts import DataSourceType, FuturesKey, DeliveryMonth
from financial_dashboard.core.interfaces.config.models import IDataSettings


class DataSettings(BaseModel, IDataSettings):
    model_config = ConfigDict(frozen=True)

    source_type: DataSourceType
    futures_key: FuturesKey
    delivery_month: DeliveryMonth
    year: dt.date

    @field_validator('source_type', mode='after')
    @classmethod
    def validate_source_type(cls, source_type: DataSourceType):
        if not isinstance(source_type, DataSourceType):
            raise TypeError(f"source_type type error: expected DataSourceType, got {type(source_type)}")
        return source_type

    @field_validator('futures_key', mode='after')
    @classmethod
    def validate_futures_key(cls, futures_key: FuturesKey):
        if not isinstance(futures_key, FuturesKey):
            raise TypeError(f"futures_key type error: expected FuturesKey, got {type(futures_key)}")
        return futures_key

    @field_validator('delivery_month', mode='after')
    @classmethod
    def validate_delivery_month(cls, delivery_month: DeliveryMonth):
        if not isinstance(delivery_month, DeliveryMonth):
            raise TypeError(f"delivery_month type error: expected DeliveryMonth, got {type(delivery_month)}")
        return delivery_month

    @field_validator('year', mode='after')
    @classmethod
    def validate_year(cls, year: dt.date):
        if not isinstance(year, dt.date):
            raise TypeError(f"year type error: expected dt.date, got {type(year)}")
        return year
