from typing import Optional
import datetime as dt
from abc import ABC


class BaseDateTimeRange(ABC):
    @property
    @abstractmethod
    def start(self) -> Optional[dt.date | dt.time]:
        ...

    @property
    @abstractmethod
    def end(self) -> Optional[dt.date | dt.time]:
        ...

class BaseFilter(ABC):
    _BASE_DATE_FILTER: Type[DateFilter] = DateFilter
    _BASE_TIME_FILTER: Type[TimeFilter] = TimeFilter

    _registry: Dict[str, Type['BaseFilter']] = {}

    def __init__(self, config: DataConfig) -> None:
        self._config = config
        self._date_range: DateRange = DateRange()
        self._time_range: TimeRange = TimeRange()

    @property
    def config(self) -> DataConfig:
        return self._config

    @property
    def start_date(self) -> Optional[dt.date]:
        """Get start date filter (applicable for all data types)."""
        return self._date_range.start

    @property
    def end_date(self) -> Optional[dt.date]:
        """Get end date filter (applicable for all data types)."""
        return self._date_range.end

    @start_date.setter
    def start_date(self, value: dt.date) -> None:
        """Set start date with validation."""
        if not isinstance(value, dt.date):
            raise TypeError(f"Expected dt.date, got {type(value)}")
        if value != self.start_date:
            start = value
            end = self.end_date
            self._date_range = BaseDateTimeRangeFactory.create(
                factory_type=DateTimeRangeFactoryType.DATE, start=start, end=end
            )

    @end_date.setter
    def end_date(self, value: dt.date) -> None:
        """Set end date with validation."""
        if not isinstance(value, dt.date):
            raise TypeError(f"Expected datetime.date, got {type(value)}")
        if value != self.end_date:
            start = self.start_date
            end = value
            self._date_range = BaseDateTimeRangeFactory.create(
                factory_type=DateTimeRangeFactoryType.DATE, start=start, end=end
            )

    @property
    @abstractmethod
    def start_time(self) -> Optional[dt.time]:
        ...

    @property
    @abstractmethod
    def end_time(self) -> Optional[dt.time]:
        ...

    @start_time.setter
    @abstractmethod
    def start_time(self, value: dt.time) -> None:
        ...

    @end_time.setter
    @abstractmethod
    def end_time(self, value: dt.time) -> None:
        ...

    @abstractmethod
    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        ...

    @classmethod
    def register(cls, source_type: str) -> Callable[[Type[FilterType]], Type[FilterType]]:
        def wrapper(subclass: Type[FilterType]) -> Type[FilterType]:
            if not issubclass(subclass, BaseFilter):
                raise TypeError(f'subclass type error: expected BaseFilter subclass, got {type(subclass)}')
            cls._registry[source_type] = subclass
            return subclass
        return wrapper

    @staticmethod
    def create(config: DataConfig) -> FilterType:
        if not isinstance(config, DataConfig):
            raise TypeError(f'config type error: expected {DataConfig.__name__}, got {type(config)}')
        if config.source_type.value not in BaseFilter._registry:
            raise ValueError(f'Unregistered source type {config.source_type.value}')
        return BaseFilter._registry[config.source_type.value](config=config)
