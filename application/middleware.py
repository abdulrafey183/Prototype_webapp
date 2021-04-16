from flask import abort, redirect, flash, url_for
from flask_login import login_required, logout_user, current_user, login_user
# from .routes import profile

class Middleware:

    @classmethod
    @login_required
    def auth(cls, user):
        pass

    @classmethod
    def authorizeSuperUser(cls, user):
        """
		Allows Authorization to only Super Uers, aborts if not super user
		@params user: current logged in user
		"""

        if user.rank: return abort(403)

    @classmethod
    def authorizeGuest(cls, user):

        if user.is_authenticated:
            flash("acc")
            return redirect(url_for('.profile'))

    