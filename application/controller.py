from flask 		 		import flash
from flask              import current_app as app
from flask_login 		import login_user
from flask_sqlalchemy   import sqlalchemy


from .model import *


def login_(email, password):

	user = User.query.filter_by(email=email).first()
	if (user and user.check_password(password1=password)):
		login_user(user)
		flash(f'Welcome {user.username}', 'success')
		return True

	flash('Invalid username/password combination', 'danger')
	return False


def editplotprice_(plot_id, price):
	db.session.query(Plot).filter_by(id=plot_id).update({'price': price})
	db.session.commit()

	flash('Plot Price Successfully Edited', 'success')


def addbuyer_(buyer):
	try:
		buyer = Buyer(
					name       = buyer['name'],
					cnic       = buyer['cnic'],
					phone	   = buyer['phone'],
					email 	   = buyer['email'],
					address    = buyer['address'],
					cnic_front = buyer['cnic_front'],
					cnic_back  = buyer['cnic_back'],
					comments   = buyer['comments']
				)

		db.session.add(buyer)
		db.session.commit()

		flash(f'Buyer with id "{buyer.id}" created', 'success')
		return True

	except sqlalchemy.exc.IntegrityError:
		flash('ERROR: A buyer with this CNIC already exists!', 'danger')
		return False

def addagent_(agent):
	try:
		agent = CommissionAgent(
					name       = agent['name'],
					cnic       = agent['cnic'],
					phone	   = agent['phone'],
					email 	   = agent['email'],
					cnic_front = agent['cnic_front'],
					cnic_back  = agent['cnic_back'],
					commission_rate = agent['commission_rate'],
					comments = agent['comments']
				)

		db.session.add(agent)
		db.session.commit()

		flash(f'Agent with id "{agent.id}" created', 'success')
		return True

	except sqlalchemy.exc.IntegrityError:
		flash('ERROR: An Agent with this CNIC already exists!', 'danger')
		return False


def savecnic(cnicfile, cnic, side):

	if not cnicfile:
		flash("ERROR: CNIC Image Missing!", "danger")
		return False

	# path to folder for storing cnic images
	cnic_file_path = app.root_path + '\\static\\img\\cnic\\agents\\' + str(cnic) + side + '.jpg'

	cnicfile.save(cnic_file_path)
	return cnic_file_path

