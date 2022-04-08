from flask       import redirect, url_for,  flash
from flask_admin import expose, AdminIndexView
from flask_login import current_user

from flask_admin.contrib.sqla import ModelView

from .middleware import Middleware

class AdminPanel(AdminIndexView):

	#Overriding Parent method
	@expose('/')
	def index(self):
		"""
		Method that Authenticates and Authorizes Super User and Renders the Admin Panel,
		Upon Authentication faiure, Redirects to login page
		Upon Authorization failure returns code 403 (forbidden reurest) 
		"""
		if current_user.is_authenticated:

			#Checking Authorization
			Middleware.authorizeSuperUser(current_user)
			
			#return super(CustomAdminIndexView, self).index()
			return self.render('admin.html')		

		flash("You must be logged in to access that page", 'danger')			
		return redirect(url_for('login'))


class ProtectedModelView(ModelView):


	#Overriding Parent method
	def is_accessible(self):

		if current_user.is_authenticated:
			#Checking Authorization
			Middleware.authorizeSuperUser(current_user)

			return True

		return False

	#Overriding Parent method
	def _handle_view(self, name):
		if not self.is_accessible():
			flash('You must be logged in to access that page', 'danger')
			return redirect(url_for('login'))