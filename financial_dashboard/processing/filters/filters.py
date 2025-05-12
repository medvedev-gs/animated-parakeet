
@dataclass(frozen=True)
class DateRange(BaseDateTimeRange):
    start: Optional[dt.date] = None
    end: Optional[dt.date] = None

    def __post_init__(self):
        if isinstance(self.start, dt.date) and isinstance(self.end, dt.date) and self.start >= self.end:
            raise ValueError("Start date must be before end date")

@dataclass(frozen=True)
class TimeRange(BaseDateTimeRange):
    start: Optional[dt.time] = None
    end: Optional[dt.time] = None

    def __post_init__(self):
        if isinstance(self.start, dt.time) and isinstance(self.end, dt.time) and self.start >= self.end:
            raise ValueError("Start time must be before end time")
