from flask              import Blueprint, redirect, render_template, flash, request, session, url_for, abort, jsonify
from flask              import current_app as app
from flask_login        import login_required, logout_user, current_user, login_user
from flask_sqlalchemy   import sqlalchemy

from .forms             import * # LoginForm, AddBuyerForm, AddDealForm, SearchBuyerForm, DeleteBuyerForm, EditBuyerForm, AddNotesForm, AddNormalUserForm, SearchForm, 
from .model             import * # db, User, Buyer, Deal, Plot, Transaction, Notes
from .middleware        import Middleware
from .                  import login_manager
from .                  import admin

import os

from datetime           import datetime
from application        import middleware


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

    #Middleware.authorizeGuest(current_user)

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password1=form.password.data):
            login_user(user)
            flash(f'Welcome {user.username}', 'success')
            return redirect(url_for('profile'))

        flash('Invalid username/password combination', 'danger')
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


@app.route('/display')
@login_required
def display():
   
    active = request.args.get("active") or "buyers"
    buyers = Buyer.query.all()
    plots  = Plot.query.all()
    CAs    = CommissionAgent.query.all()
    ETs    = Expenditure.query.all()

    filterPlotForm = FilterPlotForm()

    return render_template('display.html', active=active, buyers=buyers, plots=plots, CAs=CAs, ETs=ETs, filterPlotForm=filterPlotForm)

# @app.route("/display/buyers")
# @login_required
# def displaybuyers():
#     form = SearchBuyerForm()
#     delete_form = DeleteBuyerForm()

#     buyers = Buyer.query.all()
#     return render_template('displaybuyers.html', buyers=buyers, form=form, delete_form=delete_form)

@app.route("/display/agents")
@login_required
def displayagents():

    form = SearchAgentForm()
    #delete_form = DeleteBuyerForm()

    agents = CommissionAgent.query.all()
    return render_template('displayagent.html', agents=agents, form=form)


@app.route("/add/buyer", methods=[GET, POST])
@login_required
def addbuyer():

    addbuyer = True
    form = AddandEditForm()

    if form.validate_on_submit():
        try:

            # if cnic image is not uploaded
            if not form.cnic_front.data or not form.cnic_back.data:
                flash("ERROR: CNIC Image Missing!", "danger")
                return render_template('addbuyerandagent.html', addagent=addagent, form=form)

            # path to folder for saving cnic images
            cnic = form.cnic.data
            cnic_file_path = app.root_path + '\\static\\img\\cnic\\buyers\\' + str(cnic)

            # saving cnic images
            form.cnic_front.data.save(cnic_file_path + 'front.jpg')
            form.cnic_back.data.save(cnic_file_path  +'back.jpg')
            
            # creating buyer object
            buyer = Buyer(
                name       = form.name.data,
                cnic       = form.cnic.data,
                phone      = form.phone.data,
                email      = form.email.data,
                address    = form.address.data,
                cnic_front = cnic_file_path + 'front.jpg',
                cnic_back  = cnic_file_path + 'back.jpg',
                comments   = form.comments.data if form.comments.data else db.null()
            )

            db.session.add(buyer)
            db.session.commit()

            flash(f"Buyer with id '{buyer.id}' created", 'success')
            return redirect(url_for('add'))

        except sqlalchemy.exc.IntegrityError:
            flash("ERROR: A buyer with this CNIC already exists!", "danger")
            return render_template('addbuyerandagent.html', addbuyer=addbuyer, form=form)         
            
    return render_template('addbuyerandagent.html', addbuyer=addbuyer, form=form)


@app.route("/add/agent", methods=[GET, POST])
@login_required
def addagent():
    print("add agent")
    addagent = True
    form = AddandEditForm()
    
    if form.validate_on_submit():        
        try:

            # if cnic image is not uploaded
            if not form.cnic_front.data or not form.cnic_back.data:
                flash("ERROR: CNIC Image Missing!", "danger")
                return render_template('addbuyerandagent.html', addagent=addagent, form=form)

            # path to folder for storing cnic images
            cnic = form.cnic.data
            cnic_file_path = app.root_path + '\\static\\img\\cnic\\agents\\' + str(cnic)

            # saving cnic images
            form.cnic_front.data.save(cnic_file_path + 'front.jpg')
            form.cnic_back.data.save(cnic_file_path  +'back.jpg')
            
            # creating agent object
            agent = CommissionAgent(
                name            = form.name.data,
                cnic            = form.cnic.data,
                phone           = form.phone.data,
                email           = form.email.data,
                cnic_front      = cnic_file_path + 'front.jpg',
                cnic_back       = cnic_file_path + 'back.jpg',
                commission_rate = form.commission_rate.data,
                comments        = form.comments.data if form.comments.data else db.null()
            )

            db.session.add(agent)
            db.session.commit()

            flash(f"Agent with id '{agent.id}' created", 'success')
            return redirect(url_for('add'))

        except sqlalchemy.exc.IntegrityError:
            flash("ERROR: A Agent with this CNIC already exists!", "danger")
            return render_template('addbuyerandagent.html', addagent=addagent, form=form)

    return render_template('addbuyerandagent.html', addagent=addagent, form=form)


@app.route('/edit/buyer/<buyer_id>', methods=[POST, GET])
@login_required
def editbuyer(buyer_id):
    
    editbuyer = True
    form  = AddandEditForm()

    buyer = Buyer.query.filter_by(id=buyer_id).first()

    # if no record of buyer with entered id is found
    if buyer is None:
        flash(f'No such buyer exists!', 'danger')
        return redirect(url_for("display"))
    
    if form.validate_on_submit():

        try:
            db.session.query(Buyer).filter_by(
                                id=buyer_id
                                ).update({ 
                                    'name'       : form.name.data,
                                    'cnic'       : form.cnic.data,
                                    'phone'      : form.phone.data,
                                    'email'      : form.email.data,
                                    'address'    : form.address.data,
                                    'comments'   : form.comments.data if form.comments.data else db.null()
            })

            db.session.commit()
            flash(f'Buyer Info with id "{buyer.id}"" Updated', 'success')
            return redirect(url_for('display'))

        except sqlalchemy.orm.exc.NoResultFound:
            flash("ERROR: A buyer with this CNIC already exists!", "danger")
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
        return redirect(url_for("display"))

    if form.validate_on_submit():

        try:
            db.session.query(CommissionAgent).filter_by(
                                id=agent_id
                                ).update({ 
                                    'name'           : form.name.data,
                                    'cnic'           : form.cnic.data,
                                    'phone'          : form.phone.data,
                                    'email'          : form.email.data,
                                    'commission_rate': form.commission_rate.data,
                                    'comments' : form.comments.data if form.comments.data else db.null()
            })

            db.session.commit()
            flash(f"Agent Info with id '{agent.id}' Updated", 'success')
            return redirect(url_for('display'))

        except sqlalchemy.orm.exc.NoResultFound:
            flash("ERROR: A agent with this CNIC already exists!", "danger")
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

    db.session.delete(buyer)
    db.session.commit()

    flash('Buyer Record Deleted!', 'danger')
    return redirect(url_for('display'))


@app.route("/delete/agent/<agent_id>", methods=[POST, GET])
@login_required
def deleteagent(agent_id):

    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)

    agent = CommissionAgent.query.filter_by(id=agent_id).first()

    # if no record of buyer with entered id is found
    if agent is None:
        flash(f'No such agent exists!', 'danger')
        return redirect(url_for("display"))

    db.session.delete(agent)
    db.session.commit()

    flash('Agent Record Deleted!', 'danger')
    return redirect(url_for('display'))


@app.route('/buyer/<buyer_id>')
@login_required
def buyerinfo(buyer_id):
    buyer_id = int(buyer_id) 
    buyer = Buyer.query.filter_by(id=buyer_id).first()

    if buyer is None:
        flash('ERROR: NO Such buyer exists', 'danger')
        
    return render_template('buyerinfo.html', buyer=buyer)

@app.route('/agent/<agent_id>')
@login_required
def agentinfo(agent_id):
    agent_id = int(agent_id) 
    agent = CommissionAgent.query.filter_by(id=agent_id).first()

    if agent is None:
        flash('ERROR: NO Such agent exists', 'danger')
        
    return render_template('agentinfo.html', agent=agent)

@app.route('/plot/<plot_id>')
@login_required
def plotinfo(plot_id):
    plot_id = int(plot_id) 
    plot = Plot.query.filter_by(id=plot_id).first()

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
        db.session.query(Plot).filter_by(id=plot_id).update({'price': form.price.data})
        db.session.commit()

        flash('Plot Price Successfully Edited', 'success')
        return redirect(url_for('plotinfo', plot_id=plot_id))

    return render_template('editplotprice.html', plot=plot, form=form)


@app.route('/add/deal', methods=[GET, POST])
@login_required
def adddeal():

    form = AddDealForm()
    if form.validate_on_submit():
        # Quering the mentioned plot and buyer returns None is no such pot exists        
        plot  = Plot .query.filter_by(id= form.plot_id .data).first()
        buyer = Buyer.query.filter_by(id= form.buyer_id.data).first()

        # Applying validity checks
        if plot is None:       
            flash(f'No plot exists with Plot ID: {form.plot_id.data}',  'danger')
            return render_template('adddeal.html', form=form)

        if buyer is None:
            flash(f'No buyer exists with Buyer ID: {form.buyer_id.data}')
            return render_template('adddeal.html', form=form)

        if not (plot.deal is None):
            flash(f'The Plot with ID {plot.id} cannot be sold')
            flash(f'Plot Status: {plot.status}')
            flash(f'Plot\'s Deal ID: {plot.deal.id}')
            return render_template('adddeal.html', form=form)


        # UPDATING CORESPONDING PLOT STATUS
        plot.status = 'sold' if form.first_amount_recieved.data == plot.price else 'in a deal'
        # db.session.commit()

        try:
            # Creating Deal object
            deal = Deal(
                # id                      = form.id.data,
                buyer_id                = form.buyer_id.data,
                plot_id                 = form.plot_id.data,
                signing_date            = datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                status                  = 'finished' if form.first_amount_recieved.data == plot.price else 'on going',
                amount_per_installment  = form.amount_per_installment.data,
                installment_frequency   = form.installment_frequency.data,
                comments                = form.comments.data if form.comments.data else db.null()
            )

            db.session.add(deal)
            db.session.commit()
            db.session.refresh(deal)

        except sqlalchemy.exc.IntegrityError:
            flash('ERROR: A deal with this ID already exists!')
            return render_template('adddeal.html', form= form)

        
        # Creating corresponding transaction
        transaction = Transaction(
            amount      = form.first_amount_recieved.data,
            date_time   = datetime.now(),
            comments    = f'Initial Transaction for Deal {deal.id}',
            deal_id     = deal.id
        )

        db.session.add(transaction)
        db.session.commit()
        flash(f'Deal with ID {deal.id} successfully created!')
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


@app.route('/add/transaction', methods=[GET, POST])
@login_required
def addtransaction():

    form = AddTransactionForm()

    if form.validate_on_submit():
        pass


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
        type = Expenditure(
                    name=form.name.data
                )
        db.session.add(type)
        db.session.commit()

        flash(f'New Expenditure Type \'{form.name.data}\' Created', 'success')
        return redirect(url_for('display', active="ETs"))


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

