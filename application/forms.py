from flask_wtf import FlaskForm
from flask import Markup
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, number_range
from flask_wtf.file import FileField, FileRequired, FileAllowed
import re

from .model import db


# custom Validators
def validate_phone_and_cnic(form, field):
		if not re.match(r'^([\s\d]+)$', field.data):
			raise ValidationError('Enter Numbers Only!')

			
#Login Form 
class LoginForm(FlaskForm):
	
    email    = StringField('Email', validators=[DataRequired(), Length(min=1, max=75)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=100)])
    submit   = SubmitField('Login')

class AddandEditForm(FlaskForm):

	name 	     = StringField('Name', validators=[DataRequired(), Length(min=1, max=75)])
	cnic 	     = StringField('CNIC', validators=[DataRequired(), Length(min=13, max=13), validate_phone_and_cnic])
	phone        = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11), validate_phone_and_cnic])
	address      = StringField('Address', validators=[])
	email        = StringField('Email', validators=[DataRequired(), Length(max=100)])
	cnic_front   = FileField('CNIC Front', validators=[])
	cnic_back    = FileField('CNIC Back', validators=[])
	comments     = TextAreaField('Comments', validators=[])
	commission_rate = FloatField('Commission Rate')

                            
#Search Buyer Form
class SearchBuyerForm(FlaskForm):

	id     = IntegerField('Buyer ID')
	name   = StringField('Name')
	search = SubmitField('Search Buyer')

class SearchAgentForm(FlaskForm):
	id     = IntegerField('Agent ID')
	name   = StringField('Name')
	search = SubmitField('Search Agent')

#Delete Buyer Form
class DeleteBuyerForm(FlaskForm):

	id     = HiddenField('buyer_id')
	delete = SubmitField('Delete Buyer')       

#Add Deal Form 
class AddDealForm(FlaskForm):

	#id 						= IntegerField('Deal ID', validators=[DataRequired()])
	buyer_id 				= IntegerField('Buyer ID', validators=[DataRequired()])
	plot_id 				= IntegerField('Plot ID', validators=[DataRequired()])
	first_amount_recieved 	= IntegerField('First Paid Amount',  validators=[DataRequired()])
	amount_per_installment 	= IntegerField('Amount per Installment', validators=[DataRequired()])
	installment_frequency 	= StringField('Installments per Year',  validators=[DataRequired()])
	comments 				= TextAreaField('Comments', validators=[])
	submit 					= SubmitField('Create Deal')

#Add Notes Form
class AddNotesForm(FlaskForm):

	title   = StringField('Title',  validators=[DataRequired()])
	content = TextAreaField('Content')
	add 	= SubmitField('Add Note') 

#Add Buyer Form
class AddNormalUserForm(FlaskForm):

	#id 	 = IntegerField('Buyer ID', validators=[DataRequired()])
	username = StringField('Username',   validators=[DataRequired(), Length(min=1, max=50)])
	email    = StringField('Email',      validators=[DataRequired(), Length(min=1, max=75)])
	password = PasswordField('Password', validators=[Length(max=100)], default='12345')
	create 	 = SubmitField('Create User')
