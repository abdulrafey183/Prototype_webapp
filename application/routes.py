from flask              import abort
from flask_login        import login_required
from flask_sqlalchemy   import sqlalchemy

from .controller        import *
#from .forms             import *
# from .middleware        import Middleware
from .                  import login_manager
from .                  import admin

import os



#Setting utility variables
GET             = 'GET'
POST            = 'POST'


###------------------------START NORMAL ROUTES------------------------###

@app.route('/'    , methods= [GET])
@app.route('/home', methods= [GET])
def home(): return redirect(url_for('login')) #render_template('home.html')


@app.route('/about', methods= [GET])
def about(): return render_template('about.html',  User= User)


@app.route('/map', methods=[GET])
@login_required
def map(): return render_template('map.html')


@login_manager.user_loader
def load_user(user_id): return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized(): return unauthorized_()


@app.route('/login', methods=[GET, POST])
def login(): return login_()


@app.route("/logout", methods=[GET])
@login_required
def logout(): return logout_()


@app.route('/profile', methods=[GET, POST])
@login_required
def profile(): return profile_()


@app.route('/display')
@login_required
def display(): return display_()


@app.route('/download/<id>', methods=[GET])
def download(id): return download_(id)  


@app.route('/analytics', methods=[GET, POST])
@login_required
def analytics(): return analytics_()

###------------------------END NORMAL ROUTES------------------------###



###------------------------START ADD ROUTES------------------------###

@app.route('/add')
@login_required
def add(): return render_template('add.html')


@app.route('/add/buyeroragent', methods=[GET, POST])
@login_required
def addbuyeroragent(): return addbuyeroragent_()


@app.route('/add/deal', methods=[GET, POST])
@login_required
def adddeal(): return adddeal_()           


@app.route('/add/transaction/expense', methods=[GET, POST])
@login_required
def addexpense(): return addexpense_()


@app.route('/add/user-or-employee', methods=[GET, POST])
@login_required
def add_user_or_employee(): return add_user_or_employee_()


@app.route('/add/transaction/receivepayment/<id>', methods=[GET, POST])
@login_required
def receivepayment(id): return receivepayment_(id)


@app.route('/add/notes', methods=[GET, POST])
@login_required
def addnotes(): return addnotes_()


@app.route("/add/expendituretype", methods=[GET, POST])
@login_required
def addexpendituretype(): return addexpendituretype_()

###------------------------END ADD ROUTES------------------------###



###------------------------START EDIT ROUTES------------------------###

@app.route("/edit/plotprice/<plot_id>", methods=[GET, POST])
@login_required
def editplotprice(plot_id): return editplotprice_(plot_id)


@app.route('/edit/<entity>/<id>', methods=[GET, POST])
@login_required
def editbuyeroragent(id, entity): return editbuyeroragent_(id, entity)


###------------------------END EDIT ROUTES------------------------###



###------------------------START INFO ROUTES------------------------###

@app.route('/notes/<note_id>', methods=[GET])
@login_required
def noteinfo(note_id): return noteinfo_(note_id)


@app.route('/buyer/<buyer_id>')
@login_required
def buyerinfo(buyer_id): return buyerinfo_(buyer_id)
   
    
@app.route('/agent/<agent_id>')
@login_required
def agentinfo(agent_id): return agentinfo_(agent_id)


@app.route('/plot/<plot_id>')
@login_required
def plotinfo(plot_id): return plotinfo_(plot_id)


@app.route('/deal/<deal_id>')
@login_required
def dealinfo(deal_id): return dealinfo_(deal_id)


@app.route('/expenditure/<expenditure_id>')
@login_required
def expenditureinfo(expenditure_id): return expenditureinfo_(expenditure_id)


@app.route('/employee/<employee_id>')
@login_required
def employeeinfo(employee_id): return employeeinfo_(employee_id)

###------------------------END INFO ROUTES------------------------###



###------------------------START DELETE ROUTES------------------------###

@app.route("/delete/buyer/<buyer_id>", methods=[POST, GET])
@login_required
def deletebuyer(buyer_id): return deletebuyer_(buyer_id)


@app.route("/delete/agent/<agent_id>", methods=[POST, GET])
@login_required
def deleteagent(agent_id): return deleteagent_(agent_id)

###------------------------END DELETE ROUTES------------------------###


@app.route('/notes/all', methods=[GET])
@login_required
def allnotes():
    notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.date_time.desc())
    return render_template('allnotes.html', notes=notes)

    
###-----WHAT IS THIS DOING???-------###
@app.route("/display/agents")
@login_required
def displayagents():

    form = SearchAgentForm()
    #delete_form = DeleteBuyerForm()

    agents = CommissionAgent.query.all()
    return render_template('displayagent.html', agents=agents, form=form)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/search', methods= [GET, POST])
@login_required
def search():

    value = f'%{SearchForm().value.data}%'

    buyers = Buyer.query.filter(
        Buyer.name.like(value) |
        Buyer.cnic.like(value) 
    
    ).all()

    plots = Plot.query.filter(
        Plot.address.like(value) 
    
    ).all()

    return render_template('test.html', buyers= buyers, plots= plots)


 
###------------------------REST ROUTES------------------------###


@app.route('/rest/filterplot/<status>', methods=[POST])
@login_required
def filterplot(status): return filterplot_(status)


@app.route('/rest/buyer/all', methods=[POST])
@login_required
def allbuyers(): return allbuyers_()
    

@app.route('/rest/plot/all', methods=[POST])
@login_required
def allplots(): return allplots_()

    
@app.route('/rest/deal/all', methods=[POST])
@login_required
def alldeals(): return alldeals_()


@app.route('/rest/CA/all', methods=[POST])
@login_required
def allCAs(): return allCAs_()


@app.route('/rest/ET/all', methods=[POST])
@login_required
def allETs(): return allETs_()


@app.route('/rest/employee/all', methods=[GET, POST])
@login_required
def allEmployees(): return allEmployees_()


@app.route('/rest/<table>/<id>', methods=[GET, POST])
@login_required
def getIDfromTable(table, id): return getIDfromTable_(table, id) 

###------------------------END REST ROUTES------------------------###
