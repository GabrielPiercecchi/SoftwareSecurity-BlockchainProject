from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
from middlewares.validation import LengthValidator

class CreateProductRequestForm(FlaskForm):
    # Form per creare una nuova richiesta di prodotto
    quantity = IntegerField('Quantity', validators=[
        DataRequired(), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')
    ], render_kw={'placeholder': '100'})

class DenyProductRequestForm(FlaskForm):
    # Form per rifiutare una richiesta di prodotto
    rejectedButton = SubmitField('Reject Request')

class CarrierAcceptRequestAndCreateDeliveryForm(FlaskForm):
    # Form per accettare una richiesta di prodotto e creare una consegna
    request_id = IntegerField(validators=[DataRequired()])
    co2_emission = IntegerField('CO2 Emission', validators=[
        DataRequired(),
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')
    ], render_kw={'placeholder': '100'})
    acceptButton = SubmitField('Accept Request')