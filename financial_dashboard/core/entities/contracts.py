from enum import Enum


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
