import datetime as dt
from pydantic import BaseModel, ConfigDict

from financial_dashboard.core.entities.contracts import DataSourceType, FuturesKey, DeliveryMonth
from financial_dashboard.core.interfaces.config.models import IDataSettings


class DataSettings(BaseModel, IDataSettings):
    model_config = ConfigDict(frozen=True)

    source_type: DataSourceType
    futures_key: FuturesKey
    delivery_month: DeliveryMonth
    year: dt.date
