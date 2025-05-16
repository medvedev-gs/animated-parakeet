import datetime as dt
from typing import Optional

from financial_dashboard.core.entities.errors import *

from financial_dashboard.core.interfaces.config.factories import IDataSettingsFactory

from financial_dashboard.core.interfaces.config.models import IDataSettings

from financial_dashboard.core.interfaces.config.models import DataSourceTypeProtocol
from financial_dashboard.core.interfaces.config.models import FuturesKeyProtocol
from financial_dashboard.core.interfaces.config.models import DeliveryMonthProtocol

from financial_dashboard.core.entities.config import DataSettings


class DataSettingsFactory(IDataSettingsFactory):
    "Data Configuration Factory"
    def __init__(
            self,
            source_type: DataSourceTypeProtocol,
            futures_key: FuturesKeyProtocol,
            delivery_month: DeliveryMonthProtocol,
            year: dt.date
    ) -> None:
        self._source_type = source_type
        self._futures_key = futures_key
        self._delivery_month = delivery_month
        self._year = year
        # Cache:
        self._data_settings_cache: Optional[IDataSettings] = None

    def clear_cache(self) -> None:
        self._data_settings_cache = None

    def _load_data(self) -> IDataSettings:
        return DataSettings(
            source_type=self._source_type,
            futures_key=self._futures_key,
            delivery_month=self._delivery_month,
            year=self._year
        )

    @property
    def data_settings(self) -> IDataSettings:
        """Creates DataSettings"""
        if self._data_settings_cache is None:
            self._data_settings_cache = self._load_data()
        return self._data_settings_cache
