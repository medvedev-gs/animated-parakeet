from core.interfaces.validators import IDataValidator
import pandas as pd

class QuikDataValidator(IDataValidator):
    def validate(self, data: pd.DataFrame):
        # Реализация проверок для QUIK данных
        ...
