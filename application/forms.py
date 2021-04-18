from flask_wtf import FlaskForm
from flask import Markup
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, HiddenField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, number_range
from flask_wtf.file import FileField, FileRequired, FileAllowed

import re

from .model import Plot, Buyer


### Custom Validators ###

# validate phone and cnic
def validate_phone_and_cnic(form, field):

	if not re.match(r'^([\s\d]+)$', field.data):
		raise ValidationError('Enter Numbers Only!')

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

	# defualt_choice = (None, 'Not Selected')
	# buyers = [(row[0], 			str(row[1])+" - "+str(row[2])) for row in Buyer.query.with_entities(Buyer.id, Buyer.name, Buyer.cnic).all()]
	# plots  = [(row[0], "Plot# "+str(row[0])+" - "+str(row[1])) for row in Plot.query.filter_by(status='not sold').with_entities(Plot.id, Plot.address).all()]

	# buyers.insert(0, defualt_choice)
	# plots.insert(0, defualt_choice)

	#buyer_id 				= IntegerField  ('Buyer ID'              , validators=[DataRequired()])
	#plot_id 				= IntegerField  ('Plot ID'               , validators=[DataRequired()])
	buyer_id 				= SelectField	('Select Buyer', default=None, validators=[DataRequired()])
	plot_id 				= SelectField   ('Select Plot' , default=None, validators=[DataRequired()])

	first_amount_recieved 	= IntegerField  ('First Paid Amount'     , validators=[DataRequired()])
	amount_per_installment 	= IntegerField  ('Amount per Installment', validators=[DataRequired()])
	installment_frequency 	= StringField   ('Installments per Year' , validators=[DataRequired()])
	comments 				= TextAreaField ('Comments'              , validators=[])
	submit 					= SubmitField   ('Create Deal')

# Add Transaction Form
class AddTransactionForm(FlaskForm):

    pass

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


#Add Transaction Form
class AddTransactionForm(FlaskForm):
	
	deal_id  = HiddenField('deal_id')
	exp_id   = HiddenField('exp_id')
	amount   = IntegerField('Amount', validators=[DataRequired(), number_range(min=0)])
	comments = TextAreaField('Comments')
	add      = SubmitField('Enter Payment')
