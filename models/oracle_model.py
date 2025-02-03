from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from middlewares.validation import LengthValidator

class CoinTransferForm(FlaskForm):
    # Form per il trasferimento di coin tra organizzazioni
    target_organization = SelectField('Select Target Organization', validators=[DataRequired()])
    amount = IntegerField('Amount to Transfer', validators=[
        DataRequired(), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')
    ], render_kw={'placeholder': '100'})