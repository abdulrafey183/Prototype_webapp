from flask              import Blueprint, redirect, render_template, flash, request, session, url_for, abort, jsonify
from flask_login        import login_required, logout_user, current_user, login_user
from flask_sqlalchemy   import sqlalchemy

from .controller        import *
from .forms             import *
from .middleware        import Middleware
from .                  import login_manager
from .                  import admin

import os


#Setting utility variables
GET  = 'GET'
POST = 'POST'


@app.route('/'    , methods= [GET])
@app.route('/home', methods= [GET])
def home():
    return render_template('home.html')


@app.route('/about', methods= [GET])
def about():
    return render_template('about.html',  User= User)


#This function should return the user for the user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    '''
    Redirect unauthorized users to Login page.
    '''
    flash('You must be logged in to access that page', 'danger')
    return redirect(url_for('login'))


@app.route('/login', methods=[GET, POST])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('profile'))  

    form = LoginForm()
    if form.validate_on_submit():        
        if login_(form.email.data, form.password.data):
            return redirect(url_for('profile'))

        return redirect(url_for('login'))  

    return render_template('loginpage.html', form=form)


@app.route('/profile', methods=[GET, POST])
@login_required
def profile(): 
    user_notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.date_time.desc()).limit(4)
    return render_template('profile.html', current_user=current_user, user_notes=user_notes)


@app.route('/notes/<note_id>', methods=[GET])
@login_required
def noteinfo(note_id):
    note = Notes.query.filter_by(id=note_id).first()

    if note is None:
        flash(f'No such note exists!', 'danger')
        return redirect(url_for('profile'))

    if note.user_id != current_user.id:
        abort(403)

    return render_template('noteinfo.html', note=note)


@app.route('/notes/all', methods=[GET])
@login_required
def allnotes():
    notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.date_time.desc())
    return render_template('allnotes.html', notes=notes)

@app.route('/map', methods=[GET])
@login_required
def map():
    return render_template('map.html')


@app.route('/add')
@login_required
def add():
    return render_template('add.html')


@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')


@app.route('/display')
@login_required
def display():
   
    active = request.args.get("active") or "buyer"
    filterPlotForm = FilterPlotForm()

    if active[-1] == '+':
        active = active[:-1]
        flash('Chose a Deal to Recieve Payment', 'info')
    elif active[-1] == '!':
        active = active[:-1]
        flash('Chose Expenditure Type of Expense', 'info')
    elif active[-1] == "~":
        active = active[:-1]
        flash('Chose a Deal to View its Analytics', 'info')

    return render_template('display.html', active=active, filterPlotForm=filterPlotForm)


@app.route("/display/agents")
@login_required
def displayagents():

    form = SearchAgentForm()
    #delete_form = DeleteBuyerForm()

    agents = CommissionAgent.query.all()
    return render_template('displayagent.html', agents=agents, form=form)


@app.route('/edit/buyer/<buyer_id>', methods=[POST, GET])
@login_required
def editbuyer(buyer_id):
    
    editbuyer = True
    form  = AddandEditForm()

    buyer = Buyer.query.filter_by(id=buyer_id).first()
    # if no record of buyer with entered id is found
    if buyer is None:
        flash(f'No such buyer exists!', 'danger')
        return redirect(url_for('display', active='buyer'))
    
    if form.validate_on_submit():
        edit = editbuyer_(buyer_id, form)
        if edit:
            return redirect(url_for('display', active='buyer'))
        else:
            return render_template('editbuyerandagent.html', editbuyer=editbuyer, entity=buyer, form=form)

    else:       
        form.comments.data   = buyer.comments
        return render_template('editbuyerandagent.html',  editbuyer=editbuyer, entity=buyer, form=form)


@app.route("/edit/agent/<agent_id>", methods=[POST, GET])
@login_required
def editagent(agent_id):
    
    editagent = True
    form  = AddandEditForm()

    agent = CommissionAgent.query.filter_by(id=agent_id).first()

    # if no record of buyer with entered id is found
    if agent is None:
        flash(f'No such agent exists!', 'danger')
        return redirect(url_for('display', active='CA'))

    if form.validate_on_submit():
        edit = editagent_(agent_id, form)
        if edit:
            return redirect(url_for('display', active='CA'))
        else:
            return render_template('editbuyerandagent.html', editagent=editagent, entity=agent, form=form) 
        
    else:
        form.comments.data = agent.comments
        return render_template('editbuyerandagent.html', editagent=editagent, entity=agent, form=form)


@app.route("/delete/buyer/<buyer_id>", methods=[POST, GET])
@login_required
def deletebuyer(buyer_id):

    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)

    buyer = Buyer.query.filter_by(id=buyer_id).first()

    # if no record of buyer with entered id is found
    if buyer is None:
        flash(f'No such buyer exists!', 'danger')
        return redirect(url_for("display"))

    deletebuyer_(buyer)
    return redirect(url_for('display', active='buyer'))


@app.route("/delete/agent/<agent_id>", methods=[POST, GET])
@login_required
def deleteagent(agent_id):

    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)

    agent = CommissionAgent.query.filter_by(id=agent_id).first()

    # if no record of buyer with entered id is found
    if agent is None:
        flash(f'No such agent exists!', 'danger')
        return redirect(url_for('display', active='CA'))

    deleteagent_(agent)
    return redirect(url_for('display'))


@app.route('/buyer/<buyer_id>')
@login_required
def buyerinfo(buyer_id):
   
    buyerinfo = True
    buyer     = Buyer.query.filter_by(id=int(buyer_id) ).first()

    if buyer is None:
        flash('ERROR: NO Such buyer exists', 'danger')
        
    return render_template('agentandbuyerinfo.html', entity=buyer, buyerinfo=buyerinfo)


@app.route('/agent/<agent_id>')
@login_required
def agentinfo(agent_id):

    agentinfo = True
    agent     = CommissionAgent.query.filter_by(id=int(agent_id)).first()

    if agent is None:
        flash('ERROR: NO Such agent exists', 'danger')
        
    return render_template('agentandbuyerinfo.html', entity=agent, agentinfo=agentinfo)


@app.route('/plot/<plot_id>')
@login_required
def plotinfo(plot_id):
    
    plot = Plot.query.filter_by(id=int(plot_id) ).first()
    if plot is None:
        flash('ERROR: NO Such plot exists', 'danger')
        
    return render_template('plotinfo.html', plot=plot)


@app.route("/edit/plotprice/<plot_id>", methods=[GET, POST])
@login_required
def editplotprice(plot_id):
    
    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)
    
    plot = Plot.query.filter_by(id=plot_id).first()

    form = SetPlotPrice(address=plot.address)
    if form.validate_on_submit():
        editplotprice_(plot_id, form.price.data)
        return redirect(url_for('plotinfo', plot_id=plot_id))

    return render_template('editplotprice.html', plot=plot, form=form)


@app.route('/add/buyer', methods=[GET, POST])
@login_required
def addbuyer():

    addbuyer = True 
    form = AddandEditForm()
    if form.validate_on_submit():
        buyer_data = form
        
        if addbuyer_(buyer_data):
            return redirect(url_for('profile')) 
        else:
            return render_template('addbuyerandagent.html', addbuyer=addbuyer, form=form) 

    return render_template('addbuyerandagent.html',  form=form, addbuyer=addbuyer)


@app.route('/add/agent', methods=[GET, POST])
@login_required
def addagent():

    addagent = True 
    form = AddandEditForm()
    if form.validate_on_submit():   
        agent_data = form
        
        if addagent_(form):
            return redirect(url_for('profile')) 
        else:
            return render_template('addbuyerandagent.html', addagent=addagent, form=form) 

    return render_template('addbuyerandagent.html',  form=form, addagent=addagent)


@app.route('/add/deal', methods=[GET, POST])
@login_required
def adddeal():

    ####---MAKE THIS PRETTY---####
    defualt_choice = (None, 'Not Selected')
    buyers = [(row[0],          str(row[1])+" - "+str(row[2])) for row in Buyer.query.with_entities(Buyer.id, Buyer.name, Buyer.cnic).all()]
    CAs    = [(row[0],          str(row[1])+" - "+str(row[2])) for row in CommissionAgent.query.with_entities(CommissionAgent.id, CommissionAgent.name, CommissionAgent.cnic).all()]
    plots  = [(row[0], "Plot# "+str(row[0])+" - "+str(row[1])) for row in Plot.query.filter_by(status='not sold').with_entities(Plot.id, Plot.address).all()]
    
    installment_frequency = [None, "Monthly", "Half Yearly", "Yearly"]

    buyers.insert(0, defualt_choice)
    CAs.insert(0, defualt_choice)
    plots.insert(0, defualt_choice)
    form = AddDealForm()
    form.buyer_id.choices = buyers
    form.plot_id.choices  = plots
    form.CA_id.choices    = CAs
    form.installment_frequency.choices = installment_frequency
    ####---MAKE THIS PRETTY---####

    if form.validate_on_submit():

        deal = {
                'plot_id'                : form.plot_id.data,
                'buyer_id'               : form.buyer_id.data,
                'CA_id'                  : form.CA_id.data,
                'plot_price'             : form.plot_price.data,
                'c_rate'                 : form.c_rate.data,
                'first_amount_recieved'  : form.first_amount_recieved.data,
                'amount_per_installment' : form.amount_per_installment.data,
                'installment_frequency'  : form.installment_frequency.data,
                'comments'               : form.comments.data,
                'attachments'            : form.attachments.data
               }

        if adddeal_(deal):
            return render_template('adddeal.html', form= form)
            
        return redirect(url_for('profile'))

    return render_template('adddeal.html', form= form)


@app.route('/dealinfo/<deal_id>')
@login_required
def dealinfo(deal_id):

    deal_id = int(deal_id) 
    deal = Deal.query.filter_by(id=deal_id).first()

    if deal is None:
        flash('ERROR: NO Such deal exists', 'danger')

    return render_template('dealinfo.html', deal=deal)


@app.route('/analytics/deal/<deal_id>')
@login_required
def dealanalytics(deal_id):

    deal_id = int(deal_id)
    transaction_data = dealanalytics_(deal_id)

    if transaction_data is None:
        flash(f'No Transaction for Deal with Id {deal_id}', 'danger')
        return render_template('dealanalytics.html')

    return render_template('dealanalytics.html', transaction=transaction_data)


@app.route('/add/transaction/receivepayment/<id>', methods=[GET, POST])
@login_required
def receivepayment(id):

    try:       
        deal = Deal.query.filter_by(id=id).first()
        form   = ReceivePaymentForm(deal_id=deal.id)
        form.deal_id.choices = [(row[0], row[0]) for row in Deal.query.with_entities(Deal.id).all()]       
           
    except AttributeError as ae:
        abort(404)

    if form.validate_on_submit():
        data = {
            'type': 'deal',
            'id'  : form.deal_id.data,
            'comments': form.comments.data,
            'amount': form.amount.data
        }
        addtransaction_(data)
        
        return redirect(url_for('profile'))        

    return render_template('receivepayment.html', form=form)


@app.route('/add/transaction/expense', methods=[GET, POST])
@login_required
def addexpense():
    
    #ET = Expenditure.query.filter_by(id=id).first()
    form    = AddExpenseForm()
    choices = [(row[0], row[1]) for row in Expenditure.query.with_entities(Expenditure.id, Expenditure.name).all()]
    choices.insert(0, (None, 'Not Selected'))
    form.ET_id.choices = choices       


    if form.validate_on_submit():
        data = {
            'type'      : 'ET',
            'name'      : form.ET_name.data,
            'id'        : form.ET_id.data,
            'comments'  : form.comments.data,
            'amount'    : form.amount.data
        }
        temp = addexpense_(data)
        if temp == 'duplicate':
            return render_template('addexpense.html', form=form, error=True)
        elif temp == 'not selected':
            return render_template('addexpense.html', form=form)
        
        return redirect(url_for('profile'))        

    return render_template('addexpense.html', form=form)


@app.route('/add/notes', methods=[GET, POST])
@login_required
def addnotes():

    form = AddNotesForm()
    if form.validate_on_submit():
        note = Notes(
            title = form.title.data,
            content = form.content.data if form.content.data else db.null(),
            date_time = datetime.now(),
            user_id = current_user.id
        )

        db.session.add(note)
        db.session.commit()

        flash(f'Note Added!', 'success')
        return redirect(url_for('profile'))


    return render_template('addnotes.html', form=form)


@app.route('/add/normaluser', methods=[GET, POST])
@login_required
def addnormaluser():

    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)
    
    form = AddNormalUserForm()
    if form.validate_on_submit():
       
        #Adding user to the Dataase
        try:
            user = User(
                username = form.username.data,
                email    = form.email.data, 
                password = form.password.data or form.password.default,
                rank     = 1
            )
            db.session.add(user)
            db.session.commit()

        except sqlalchemy.exc.IntegrityError as ie:
            flash('User with emil already exists', 'danger')
            return render_template('addnormaluser.html', form=form)

        
        flash(f'Normal User Created!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('addnormaluser.html', form=form)


@app.route("/add/expendituretype", methods=[GET, POST])
@login_required
def addexpendituretype():

    form = AddExpendituretypeForm()
    if form.validate_on_submit():
        data = {
            'name'  : form.name.data,
            'flash' : True 
        }
        if addexpenditure_(data) is not None: 
            return redirect(url_for('display', active="ET"))

    return render_template('addexpendituretype.html', form=form)


@app.route("/logout", methods=[GET])
@login_required
def logout():
    logout_user()
    flash('User logged out', 'info')
    return redirect(url_for('home'))


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


@app.route('/rest/filterplot/<status>', methods=[POST])
@login_required
def filterplot(status):

    plots = Plot.query.all() if status=='all' else Plot.query.filter_by(status=status).all()

    return jsonify(json_list=[plot.serialize for plot in plots])


@app.route('/rest/buyer/all', methods=[POST])
@login_required
def allbuyers():

    buyers = Buyer.query.all()
    return jsonify(json_list=[buyer.serialize for buyer in buyers])


@app.route('/rest/plot/all', methods=[POST])
@login_required
def allplots():

    plots = Plot.query.all()
    print(len(plots))
    return jsonify(json_list=[plot.serialize for plot in plots])


@app.route('/rest/deal/all', methods=[POST])
@login_required
def alldeals():

    deals = Deal.query.all()
    return jsonify(json_list=[deal.serialize for deal in deals])



@app.route('/rest/CA/all', methods=[POST])
@login_required
def allCAs():

    CAs = CommissionAgent.query.all()
    return jsonify(json_list=[CA.serialize for CA in CAs])


@app.route('/rest/ET/all', methods=[POST])
@login_required
def allETs():

    ETs = Expenditure.query.all()
    return jsonify(json_list=[ET.serialize for ET in ETs])


@app.route('/rest/<table>/<id>', methods=[GET, POST])
@login_required
def getIDfromTable(table, id):

    exec(f"locals()['temp'] = {table}.query.filter_by(id={id}).first()")
    
    return jsonify(json_list=[locals()['temp'].serialize])


