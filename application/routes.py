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
defualt_choice  = (None, 'Not Selected')

###------------------------NORMAL ROUTES------------------------###

@app.route('/'    , methods= [GET])
@app.route('/home', methods= [GET])
def home(): return render_template('home.html')


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

###------------------------END NORMAL ROUTES------------------------###



###------------------------ADD ROUTES------------------------###

@app.route('/add')
@login_required
def add(): return render_template('add.html')


@app.route('/add/buyeroragent', methods=[GET, POST])
@login_required
def addbuyeroragent(): return addbuyeroragent_()


@app.route('/add/deal', methods=[GET, POST])
@login_required
def adddeal():

    ####---MAKE THIS PRETTY---####
    buyers = [(buyer.id    , str(buyer.person.name)+" - "+str(buyer.person.cnic)) for buyer in Buyer.query.all()]
    CAs    = [(CA.person_id, str(CA.person.name)   +" - "+str(CA.person.cnic))    for CA in CommissionAgent.query.all()]
    
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


###------------------------END ADD ROUTES------------------------###



###------------------------EDIT ROUTES------------------------###

@app.route("/edit/plotprice/<plot_id>", methods=[GET, POST])
@login_required
def editplotprice(plot_id): return editplotprice_(plot_id)


@app.route('/edit/<entity>/<id>', methods=[GET, POST])
@login_required
def editbuyeroragent(id, entity): return editbuyeroragent_(id, entity)


###------------------------EDIT ROUTES------------------------###



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






@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')
   
    

@app.route("/display/agents")
@login_required
def displayagents():

    form = SearchAgentForm()
    #delete_form = DeleteBuyerForm()

    agents = CommissionAgent.query.all()
    return render_template('displayagent.html', agents=agents, form=form)


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

    agent = CommissionAgent.query.filter_by(person_id=agent_id).first()

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
    agent     = CommissionAgent.query.filter_by(person_id=int(agent_id)).first()

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


@app.route('/deal/<deal_id>')
@login_required
def dealinfo(deal_id):

    deal_id = int(deal_id) 
    deal = Deal.query.filter_by(id=deal_id).first()

    transaction_data = dealanalytics_(deal_id)

    if deal is None:
        flash('ERROR: NO Such deal exists', 'danger')

    return render_template('dealinfo.html', deal=deal, transaction=transaction_data)


'''@app.route('/deal/analytics/<deal_id>')
@login_required
def dealanalytics(deal_id):

    deal_id = int(deal_id)
    transaction_data = dealanalytics_(deal_id)

    if transaction_data is None:
        flash(f'No Transaction for Deal with Id {deal_id}', 'danger')
        return render_template('dealanalytics.html')

    return render_template('dealanalytics.html', transaction=transaction_data)'''


@app.route('/analytics/expenditure/macro', methods=[GET, POST])
@login_required
def expenditure_macro_analytics():    

    form = MacroAnalyticsForm()
    if form.validate_on_submit():
        print("\n\n\n", form.shortcuts.data)
        print(form.start.data)
        print(form.end.data, "\n\n\n")

    return render_template('expenditure-macro-analytics.html', form=form)


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
    
    
    ###-----MAKE THIS PRETTY-----###
    ETs       = [(row[0], row[1])            for row in Expenditure.query.with_entities(Expenditure.id, Expenditure.name).all()]
    employees = [(user.id, user.person.name) for user in User.query.filter_by(rank=2).all() ]
    ETs.insert      (0, defualt_choice)
    employees.insert(0, defualt_choice)

    form                    = AddExpenseForm()
    form.employee.choices   = employees
    form.ET_id.choices      = ETs        
    ###-----MAKE THIS PRETTY-----###      


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


@app.route('/add/user-or-employee', methods=[GET, POST])
@login_required
def add_user_or_employee():

    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)

    form = AddUserOrEmployeeForm()
    form.name.label = 'Username'
    if form.validate_on_submit():
        data = {
            'type'      : int(form.type.data),
            'name'  : form.name.data,
            'email'     : form.email.data,
            'password'  : form.password.data or '12345',
            'cnic'      : form.cnic.data,
            'phone'     : form.phone.data,
            'cnic_front': form.cnic_front.data,
            'cnic_back' : form.cnic_back.data,
            'comments'  : form.comments.data or db.null()
        }
        if add_user_or_employee_(data) is None:
            return redirect(url_for('profile'))        
    
    return render_template('add-user-or-employee.html', form=form)


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


@app.route('/rest/<table>/<id>', methods=[GET, POST])
@login_required
def getIDfromTable(table, id): return getIDfromTable_(table, id)

###------------------------REST ROUTES------------------------###
