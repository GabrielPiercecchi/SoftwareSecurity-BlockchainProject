from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField
from middlewares.validation import LengthValidator

class ProductForm(FlaskForm):
    # Form per la creazione di un nuovo prodotto
    name = StringField('Product Name', validators=[DataRequired()], render_kw={'placeholder': 'Name'})
    type = SelectField('Type', choices=[('raw material', 'Raw Material'), ('end product', 'End Product')], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')
    ], render_kw={'placeholder': '100'})
    co2_production_product = IntegerField('CO2 Production', validators=[
        DataRequired(), 
        NumberRange(min=1, message='The value must be greater than 0'),
        LengthValidator(max_length=10, message='The value must be less than 10 digits')
    ], render_kw={'placeholder': '100'})
    co2_origin_product_list = SelectMultipleField('CO2 Origin Products', choices=[])

class UpdateProductForm(FlaskForm):
    # Form per l'aggiornamento di un prodotto esistente
    name = StringField('Organization Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('raw material', 'Raw material'), ('end product', 'End product')], validators=[DataRequired()])