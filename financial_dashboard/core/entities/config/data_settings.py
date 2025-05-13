import datetime as dt
from pydantic import BaseModel, ConfigDict

from financial_dashboard.core.interfaces.config.models import DataSourceTypeProtocol
from financial_dashboard.core.interfaces.config.models import FuturesKeyProtocol
from financial_dashboard.core.interfaces.config.models import DeliveryMonthProtocol
from financial_dashboard.core.interfaces.config.models import IDataSettings


class DataSettings(BaseModel, IDataSettings):
    "Configuration file"
    model_config = ConfigDict(frozen=True)

    source_type: DataSourceTypeProtocol
    futures_key: FuturesKeyProtocol
    delivery_month: DeliveryMonthProtocol
    year: dt.date
