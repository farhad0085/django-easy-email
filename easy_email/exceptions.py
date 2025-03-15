class BaseException(Exception):
    """The base exception used in the system."""
    
    def __init__(self, msg=None):
        # Default message if none is provided
        if msg is None:
            msg = "An error occurred in the system"
        super().__init__(msg)


class TemplateNotFound(BaseException):
    """The exception raised when a template is not found."""
    
    def __init__(self, template_name=None):
        msg = f"Template '{template_name}' doesn't exist" if template_name else "Template doesn't exist"
        super().__init__(msg)


class InvalidSendTime(BaseException):
    """Raised when the specified send time is in the past."""
    
    def __init__(self, datetime_value=None):
        try:
            msg = f"The specified datetime '{datetime_value}' is in the past" if datetime_value else "The specified send time is invalid"
        except:
            msg = "The specified send time is invalid"
        super().__init__(msg)
