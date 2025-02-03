from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
from middlewares.validation import LengthValidator

class AcceptCoinRequestForm(FlaskForm):
    request_id = IntegerField('Request ID', validators=[DataRequired()])
    submit = SubmitField('Accept')

class CoinRequestForm(FlaskForm):
    coin = IntegerField('Coin', validators=[DataRequired(message='You must digit an Integer number'), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')], 
        render_kw={'placeholder': '100'})
    submit = SubmitField('Submit')