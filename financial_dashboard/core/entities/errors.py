
class CustomValueError(ValueError):
    ...

class UnregisteredSourceTypeError(CustomValueError):
    ...

class CustomTypeError(TypeError):
    ...

class DataSourceTypeError(CustomTypeError):
    """Исключение, вызываемое при несоответствии типа source_type."""
    pass

class FuturesKeyError(CustomTypeError):
    """Исключение, вызываемое при несоответствии типа futures_key."""
    pass

class DeliveryMonthError(CustomTypeError):
    """Исключение, вызываемое при несоответствии типа delivery_month."""
    pass

class DataSettingsFactoryError(CustomTypeError):
    """Исключение, вызываемое при несоответствии типа data_settings_factory."""
    pass

class IParseSettingsTemplateError(CustomTypeError):
    """Исключение, вызываемое при несоответствии типа data_settings_factory."""
    pass
