from flask_wtf 			import FlaskForm
from wtforms 			import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, HiddenField, SelectField, ValidationError, MultipleFileField, DateField
from wtforms.validators import DataRequired, Length, number_range, Optional
from flask_wtf.file 	import FileField, FileRequired, FileAllowed

from .model   import db, Plot, Buyer
from .utility import validate_phone_and_cnic


#Login Form 
class LoginForm(FlaskForm):
	
    email    = StringField  ('Email'   , validators=[DataRequired(), Length(min=1, max=75)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=100)])
    submit   = SubmitField  ('Login')


class AddPersonForm(FlaskForm):

	name 	     = StringField  ('Name',        validators=[DataRequired(), Length(min=1, max=75)])
	email        = StringField  ('Email',       validators=[DataRequired(), Length(max=75)])
	cnic 	     = StringField  ('CNIC',        validators=[DataRequired(), Length(min=13, max=13), validate_phone_and_cnic])
	phone        = StringField  ('Phone',       validators=[DataRequired(), Length(min=11, max=11), validate_phone_and_cnic])
	cnic_front   = FileField    ('CNIC Front',  validators=[DataRequired(), FileAllowed(['jpeg','png', 'jpg', 'pdf'], 'File Format Not Allowed')])
	cnic_back    = FileField    ('CNIC Back',   validators=[DataRequired(), FileAllowed(['jpeg','png', 'jpg', 'pdf'], 'File Format Not Allowed')])
	
	comments     = TextAreaField('Comments',    validators=[])

#Add User or Employee Form
class AddUserOrEmployeeForm(AddPersonForm):

	#Overriding Parent Class Fields
	email      = StringField  ('Email'     ,  validators=[Optional(), Length(min=1, max=75)] )
	cnic_front = FileField    ('CNIC Front',  validators=[Optional(), FileAllowed(['jpeg','png', 'jpg', 'pdf'], 'File Format Not Allowed')])
	cnic_back  = FileField    ('CNIC Back' ,  validators=[Optional(), FileAllowed(['jpeg','png', 'jpg', 'pdf'], 'File Format Not Allowed')])

	type       = SelectField  ('Chose Type',  choices=[(1, 'User'), (2, 'Employee')], default=1)
	password = PasswordField('Password'  , validators=[Length(max=100)], default='12345')
	create 	 = SubmitField  ('Add')

#Add and Edit Buyer or Commission Agent Form
class AddandEditBuyerorAgentForm(AddPersonForm):

	entity       = SelectField('Add Record As', choices=['Buyer', 'Commission Agent'], default='Buyer', validators=[DataRequired()])
	address      = StringField('Address',       validators=[])
	
# #Search Buyer Form
# class SearchBuyerForm(FlaskForm):

# 	id     = IntegerField('Buyer ID')
# 	name   = StringField ('Name')
# 	search = SubmitField ('Search Buyer')

# class SearchAgentForm(FlaskForm):

# 	id     = IntegerField('Agent ID')
# 	name   = StringField ('Name')
# 	search = SubmitField ('Search Agent')

#Delete Buyer Form
class DeleteBuyerForm(FlaskForm):

	id     = HiddenField('buyer_id')
	delete = SubmitField('Delete Buyer')

#Add Deal Form 
class AddDealForm(FlaskForm):
	
	#buyer_id 				= IntegerField  ('Buyer ID'              , validators=[DataRequired()])
	#plot_id 				= IntegerField  ('Plot ID'               , validators=[DataRequired()])

	buyer_id 				= SelectField		('Select Buyer'			        , default=None, validators=[DataRequired()])
	plot_id 				= SelectField   	('Select Plot' 			        , default=None, validators=[DataRequired()])
	c_rate					= FloatField		('Commission Rate'		        , default=0   , validators=[number_range(min=0, max=1)])
	CA_id 					= SelectField		('Select Commission Agent'      , default=None)
	plot_price				= IntegerField		('Plot Price'                   , default=0)
	first_amount_recieved 	= IntegerField  	('First Paid Amount (optional)' , default=0)
	amount_per_installment 	= IntegerField  	('Expected Amount per Installment (optional)', default=0)
	installment_frequency 	= SelectField   	('Expected Number of Installments per Year (optional)', default=None)
	comments 				= TextAreaField 	('Comments')
	attachments 			= MultipleFileField	('Attachments')
	submit 					= SubmitField   	('Create Deal')
	
	
	
#Add Transaction Form
class AddTransactionForm(FlaskForm):

	amount   = IntegerField ('Amount', validators=[DataRequired(), number_range(min=0)])
	comments = TextAreaField('Comments')
	add      = SubmitField  ('Add')


class ReceivePaymentForm(AddTransactionForm):

	deal_id = SelectField('Deal', default=db.null())


class AddExpenseForm(AddTransactionForm):

	ET_id    = SelectField('Expenditure Type'           , default=None)
	employee = SelectField  ('Choose Employee')
	ET_name  = StringField('Create New Expenditure Type', validators=[Length(max=100)])


# Add Notes Form
class AddNotesForm(FlaskForm):

	title   = StringField  ('Title',  validators=[DataRequired()])
	content = TextAreaField('Content')
	add 	= SubmitField  ('Add Note')


#Set Plot Price Form
class SetPlotPrice(FlaskForm):
	
	address = SelectField   ('Address', choices=[row[0] for row in Plot.query.with_entities(Plot.address).all()])
	price   = IntegerField  ('Price',  validators=[DataRequired(), number_range(min=0) ])
	set     = SubmitField   ('Set Price')

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


#Macro Analytics Form
class MacroAnalyticsForm(FlaskForm):
 
	choices = [ (1, 'Last 7 Days'), (2, 'Last 14 Days'), (3, 'Last 30 Days'), (4, 'Last 3 Months'), (5, 'Last 6 Months'), (7, 'All Time'), (8, 'Custom') ]

	shortcuts 	= SelectField('Chose a Time Period', choices=choices, validators=[DataRequired()])

	start 		= DateField('From', format='%Y-%m-%d', validators=[Optional()])
	end 		= DateField('To'  , format='%Y-%m-%d', validators=[Optional()])
	show 		= SubmitField('Show')


