from flask 		 		import flash
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


def addbuyer_(name, cnic, comments):
	try:
		buyer = Buyer(
					name     = name,
					cnic     = cnic,
					comments = comments if comments else db.null()
				)

		db.session.add(buyer)
		db.session.commit()

		flash(f'Buyer with id "{buyer.id}" created', 'success')
		return True

	except sqlalchemy.exc.IntegrityError:
		flash('ERROR: A buyer with this CNIC already exists!', 'danger')
		return False

