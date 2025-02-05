from wtforms.validators import ValidationError
import re
from flask import flash

class LengthValidator:
    # Validatore personalizzato per controllare la lunghezza massima di un campo
    def __init__(self, max_length, message=None):
        self.max_length = max_length
        if not message:
            message = f'Field cannot be longer than {max_length} characters.'
        self.message = message

    def __call__(self, form, field):
        # Verifica se la lunghezza del campo supera la lunghezza massima
        if len(str(field.data)) > self.max_length:
            flash(self.message, 'length_error')
            raise ValidationError(self.message)
        
class PhoneNumberValidator:
    # Validatore personalizzato per controllare il formato del numero di telefono
    def __init__(self, message=None):
        if not message:
            message = 'Invalid phone number format. It should start with + followed by digits.'
        self.message = message

    def __call__(self, form, field):
        # Verifica se il numero di telefono inizia con + e contiene solo numeri
        if not re.match(r'^\+\d+$', field.data):
            flash(self.message, 'wrong_telephone')
            raise ValidationError(self.message)