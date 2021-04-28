from flask_wtf import FlaskForm
from flask import Markup
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, HiddenField, SelectField, ValidationError, MultipleFileField
from wtforms.validators import DataRequired, Length, number_range
from flask_wtf.file import FileField, FileRequired, FileAllowed

import re

from .model   import db, Plot, Buyer
from .utility import validate_phone_and_cnic


### Forms

#Login Form 
class LoginForm(FlaskForm):
	
    email    = StringField  ('Email'   , validators=[DataRequired(), Length(min=1, max=75)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=100)])
    submit   = SubmitField  ('Login')

class AddandEditForm(FlaskForm):

	name 	     = StringField('Name', validators=[DataRequired(), Length(min=1, max=75)])
	cnic 	     = StringField('CNIC', validators=[DataRequired(), Length(min=13, max=13), validate_phone_and_cnic])
	phone        = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11), validate_phone_and_cnic])
	address      = StringField('Address', validators=[])
	email        = StringField('Email', validators=[DataRequired(), Length(max=100)])
	cnic_front   = FileField('CNIC Front', validators=[FileAllowed(['jpeg','png'], 'Image Files Only')])
	cnic_back    = FileField('CNIC Back', validators=[FileAllowed(['jpeg','png'], 'Image Files Only')])
	comments     = TextAreaField('Comments', validators=[])
                           
#Search Buyer Form
class SearchBuyerForm(FlaskForm):

	id     = IntegerField('Buyer ID')
	name   = StringField ('Name')
	search = SubmitField ('Search Buyer')

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
	
	#buyer_id 				= IntegerField  ('Buyer ID'              , validators=[DataRequired()])
	#plot_id 				= IntegerField  ('Plot ID'               , validators=[DataRequired()])

	buyer_id 				= SelectField		('Select Buyer'			  , default=None, validators=[DataRequired()])
	plot_id 				= SelectField   	('Select Plot' 			  , default=None, validators=[DataRequired()])
	c_rate					= FloatField		('Commission Rate'		  , default=0   , validators=[number_range(min=0, max=1)])
	CA_id 					= SelectField		('Select Commission Agent', default=None)
	plot_price				= IntegerField		('Plot Price', default=0)
	first_amount_recieved 	= IntegerField  	('First Paid Amount (optional)', default=0)
	amount_per_installment 	= IntegerField  	('Expected Amount per Installment (optional)', default=0)
	installment_frequency 	= SelectField   	('Expected Number of Installments per Year (optional)', default=None)
	comments 				= TextAreaField 	('Comments')
	attachments 			= MultipleFileField	('Attachments')
	submit 					= SubmitField   	('Create Deal')
	
	
	
#Add Transaction Form
class AddTransactionForm(FlaskForm):

	amount   = IntegerField('Amount', validators=[DataRequired(), number_range(min=0)])
	comments = TextAreaField('Comments')
	add      = SubmitField('Add')


class ReceivePaymentForm(AddTransactionForm):

	deal_id = SelectField('Deal', default=db.null())


class AddExpenseForm(AddTransactionForm):

	ET_id = SelectField('Expenditure Type', default=db.null())


# Add Notes Form
class AddNotesForm(FlaskForm):

	title   = StringField  ('Title',  validators=[DataRequired()])
	content = TextAreaField('Content')
	add 	= SubmitField  ('Add Note')

#Add Buyer Form
class AddNormalUserForm(FlaskForm):

	#id 	 = IntegerField('Buyer ID', validators=[DataRequired()])
	username = StringField('Username',   validators=[DataRequired(), Length(min=1, max=50)])
	email    = StringField('Email',      validators=[DataRequired(), Length(min=1, max=75)])
	password = PasswordField('Password', validators=[Length(max=100)], default='12345')
	create 	 = SubmitField('Create User')

#Set Plot Price Form
class SetPlotPrice(FlaskForm):
	
	address = SelectField('Address', choices=[row[0] for row in Plot.query.with_entities(Plot.address).all()])
	price   = IntegerField('Price',  validators=[DataRequired()])
	set     = SubmitField('Set Price')

#Add Expenditure Type Form
class AddExpendituretypeForm(FlaskForm):

	name = StringField('Name of Expenditure', validators=[DataRequired(), Length(min=1, max=100)])
	add  = SubmitField('Add Expenditure Type')

# search form
class SearchForm(FlaskForm):

    value  = StringField('Value', validators= [DataRequired()])
    search = SubmitField('Search')


#Filter Plot by Status Form
class FilterPlotForm(FlaskForm):

	status = SelectField('Filter By:', choices=[('all', 'All'), ('sold','Sold'), ('not sold','Not Sold'), ('in a deal','In a Deal')])
	filter = SubmitField('Filter')



