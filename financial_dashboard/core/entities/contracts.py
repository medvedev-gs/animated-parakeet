from enum import Enum


class ColumnNames:
    TICKER: str = 'Ticker'
    PER: str = 'Per'
    DATE: str = 'Date'
    TIME: str = 'Time'
    OPEN: str = 'Open'
    HIGH: str = 'High'
    LOW: str = 'Low'
    CLOSE: str = 'Close'
    VOL: str = 'Volume'
    BOARDID: str = 'BoardID'
    OPENPOSITIONVALUE: str = 'OpenPositionValue'
    VALUE: str = 'Value'
    OPENPOSITION: str = 'OpenPosition'
    SETTLEPRICE: str = 'SettlePrice'
    WAPRICE: str = 'WAPrice'
    SETTLEPRICEDAY: str = 'SettlePriceDay'
    CHANGE: str = 'Change'
    QTY: str = 'QTY'
    NUMTRADES: str = 'NumTrades'


class DataSourceType(str, Enum):
    """Enum representing available data source types.
    
    Attributes:
        QUIK: Data from QUIK trading system
        DAILY: Daily aggregated data
    """
    QUIK = 'quik'
    DAILY = 'daily'


class FuturesKey(str, Enum):
    """Enum representing futures contract symbols.
    
    Attributes:
        RI: RTS Index futures
        MX: MOEX Index futures  
        Si: USD/RUB futures
    """
    RI = 'RI'
    MX = 'MX'
    Si = 'Si'
    CR = 'CR'
    SF = 'SF'
    NA = 'NA'
    BR = 'BR'
    NG = 'NG'
    GD = 'GD'
    SV = 'SV'
    SR = 'SR'
    GZ = 'GZ'
    LK = 'LK'


class DeliveryMonth(str, Enum):
    """Enum representing futures delivery months.
    
    Uses standard futures month codes:
        H: March
        M: June  
        U: September
        Z: December
    """
    F = 'F'
    G = 'G'
    H = 'H'
    J = 'J'
    K = 'K'
    M = 'M'
    N = 'N'
    Q = 'Q'
    U = 'U'
    V = 'V'
    X = 'X'
    Z = 'Z'
