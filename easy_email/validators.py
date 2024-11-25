import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class TemplateNameValidator:
    """
    Validator for Template model's name field.
    Ensures that the name:
    - Contains only lowercase letters, numbers, and underscores.
    - Does not start with a number.
    """
    message = (
        "Name can only contain underscores (_), lowercase letters, and numbers, "
        "and cannot start with a number."
    )
    pattern = r'^[a-z_][a-z0-9_]*$'
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not re.fullmatch(self.pattern, value):
            raise ValidationError(self.message, code=self.code)
