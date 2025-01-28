from wtforms.validators import ValidationError

class LengthValidator:
    def __init__(self, max_length, message=None):
        self.max_length = max_length
        if not message:
            message = f'Field cannot be longer than {max_length} characters.'
        self.message = message

    def __call__(self, form, field):
        if len(str(field.data)) > self.max_length:
            raise ValidationError(self.message)