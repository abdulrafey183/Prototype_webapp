from flask              import flash, send_file, render_template, redirect, url_for, request, jsonify
from flask              import current_app as app 
from flask_login        import login_user, current_user, logout_user
from flask_sqlalchemy   import sqlalchemy
from sqlalchemy.exc     import IntegrityError

from .model             import *
from .utility           import *
from .forms             import *
from .middleware        import Middleware


from datetime import datetime
from io       import  BytesIO


defualt_choice  = (None, 'Not Selected')


###------------------------NORMAL ROUTES------------------------###
def unauthorized_():
    flash('You must be logged in to access that page', 'danger')
    return redirect(url_for('login'))

 
def login_():

    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Person.query.filter(Person.email==form.email.data).first().user[0] 
            if (user and user.check_password(password1=form.password.data)):
                login_user(user)
                flash(f'Welcome {user.person.name}', 'success')        
                return redirect(url_for('profile'))

        except (IndexError, AttributeError):
            flash('No Such User', 'danger')
            return redirect(url_for('login')) 

        flash('Invalid password combination', 'danger')
        return redirect(url_for('login'))  

    return render_template('loginpage.html', form=form)


def logout_():
    logout_user()
    flash('User logged out', 'info')
    return redirect(url_for('home'))


def profile_():
    user_notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.date_time.desc()).limit(4)
    return render_template('profile.html', current_user=current_user, user_notes=user_notes)


def display_():
    active = request.args.get("active") or "buyer"
    filterPlotForm = FilterPlotForm()

    if active[-1] == '+':
        active = active[:-1]
        flash('Chose a Deal to Recieve Payment', 'info')
    elif active[-1] == "~":
        active = active[:-1]
        flash('Chose a Deal to View its Analytics', 'info')

    return render_template('display.html', active=active, filterPlotForm=filterPlotForm)


def download_(id):

    file = File.query.filter_by(id=id).first()
    return send_file(BytesIO(file.data), attachment_filename=file.filename, as_attachment=True)
    

###------------------------END NORMAL ROUTES------------------------###

###------------------------EDIT ROUTES------------------------###

def editplotprice_(plot_id):

    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)
    
    plot = Plot.query.filter_by(id=plot_id).first()
    if plot.status != 'not sold':
        flash('Plot Price Cannot be Changed Because Plot is in a Deal', 'danger')
        return redirect(url_for('plotinfo', plot_id=plot_id))   

    form = SetPlotPrice(address=plot.address)
    if form.validate_on_submit():
   
        db.session.query(Plot).filter_by(id=plot_id).update({'price': form.price.data})
        db.session.commit()

        flash('Plot Price Successfully Edited', 'success')
        return redirect(url_for('plotinfo', plot_id=plot_id))

    return render_template('editplotprice.html', plot=plot, form=form)

###------------------------END EDIT ROUTES------------------------###

###------------------------ADD ROUTES------------------------###

def adddeal_():

    buyers = [(buyer.id    , str(buyer.person.name)+" - "+str(buyer.person.cnic)) for buyer in Buyer.query.all()]
    CAs    = [(CA.person_id, str(CA.person.name)   +" - "+str(CA.person.cnic))    for CA    in CommissionAgent.query.all()]    
    plots  = [(plot.id     , "Plot# "+str(plot.id) +" - "+plot.address)           for plot  in Plot.query.filter_by(status='not sold').all()]
    
    installment_frequency = [None, "Monthly", "Half Yearly", "Yearly"]

    buyers.insert(0, defualt_choice)
    CAs.insert   (0, defualt_choice)
    plots.insert (0, defualt_choice)

    form = AddDealForm()

    form.buyer_id.choices = buyers
    form.plot_id.choices  = plots
    form.CA_id.choices    = CAs

    form.installment_frequency.choices = installment_frequency

    if form.validate_on_submit():

        plot  = Plot.query.filter_by(id=form.plot_id.data).first()
        buyer = Buyer.query.filter_by(id=form.buyer_id.data).first()
        CA    = CommissionAgent.query.filter_by(person_id=form.CA_id.data).first()

        if plot is None:
            flash('No Plot Selected', 'danger')
            return render_template('adddeal.html', form= form)
        elif buyer is None:
            flash('No Buyer Selected', 'danger')
            return render_template('adddeal.html', form= form)


        # Setting the plot price according to the price provided by user
        db.session.query(Plot).filter_by(id=form.plot_id.data).update(
            {'price': form.plot_price.data})
        db.session.commit()
        db.session.refresh(plot)

        # UPDATING CORESPONDING PLOT AND DEAL STATUS
        if (form.first_amount_recieved.data == plot.price):
            plot.status = 'sold'
            deal_status = 'completed'
        else:
            plot.status = 'in a deal'
            deal_status = 'on going'

        db.session.add(plot)


        # Creating Deal and adding to Database
        deal = Deal(
            status                  = deal_status,
            signing_date            = datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            amount_per_installment  = form.amount_per_installment.data  or db.null(),
            installment_frequency   = form.installment_frequency.data   or db.null(),
            commission_rate         = form.c_rate.data                  or db.null(),
            comments                = form.comments.data                or db.null(),
            buyer_id                = form.buyer_id.data,
            plot_id                 = form.plot_id.data,
            commission_agent_id     = (CA and CA.person_id) or db.null(),
        )

        db.session.add(deal)
        db.session.commit()
        db.session.refresh(deal)

        # Adding Deal Attachments to the Database
        for attachment in form.attachments.data:
            file = File(
                filename    = attachment.filename,
                format      = attachment.filename.split('.')[-1],
                data        = attachment.read(),
                deal_id     = deal.id,
                person_id   = db.null()
            )
            db.session.add(file)

        # Creating corresponding transaction and adding to Database
        transaction = Transaction(
            amount          = form.first_amount_recieved.data,
            date_time       = datetime.now(),
            comments        = f'Initial Transaction for Deal {deal.id}',
            deal_id         = deal.id,
            expenditure_id  = db.null()
        )

        db.session.add(transaction)
        db.session.commit()

        flash(f'Deal with ID {deal.id} successfully created!', 'success')
        return redirect(url_for('profile'))

    return render_template('adddeal.html', form= form)



###------------------------END ADD ROUTES------------------------###
    
def addbuyeroragent_():

    form = AddandEditBuyerorAgentForm()

    if form.validate_on_submit():

        try:
            entity = form.entity.data
            person_id = addperson(form)

            if entity == 'Buyer':
                active = 'buyer'
                db_entity = Buyer(
                    address    = form.address.data,
                    person_id  = person_id                
                )

            elif entity == 'Commission Agent':
                active = 'CA'
                db_entity = CommissionAgent(
                    person_id = person_id
                )

            db.session.add(db_entity)
            db.session.commit()

            addfile(person_id, form.cnic.data, form.cnic_front.data, 'front')
            addfile(person_id, form.cnic.data, form.cnic_back.data, 'back')

            if entity == 'Commission Agent':
                id = db_entity.person.id
            else:
                id = db_entity.id

            flash(f'SUCCESS: {entity} "{form.name.data}" added to record', 'success')
            return redirect(url_for('display', active=active))
        
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash(f'ERROR: A {entity} with the entered credentials already exists!', 'danger')
    
    return render_template('addbuyerandagent.html',  form=form)


def editbuyeroragent_(id, entity):

    form = AddandEditBuyerorAgentForm()
    db_entity = None

    if entity == 'Buyer':
        db_entity = Buyer.query.filter_by(person_id=id).first()
        active = 'buyer'
    elif entity == 'Commission Agent':
        db_entity = CommissionAgent.query.filter_by(person_id=id).first()
        active = 'CA'

    # if no record of entity with entered id is found
    if db_entity is None:
        flash(f'No such {entity} exists!', 'danger')
        return redirect(url_for('display', active=active))
    
    if form.validate_on_submit():

        try:
            db.session.query(Person).filter_by(id=id).update({
                'name': form.name.data,
                'cnic': form.cnic.data,
                'phone': form.phone.data,
                'email': form.email.data,
                'comments': form.comments.data if form.comments.data else db.null()
            })

            if form.entity.data == 'Buyer':
                entity_type = 'Buyer'

                db.session.query(Buyer).filter_by(
                            person_id=id
                            ).update({'address': form.address.data})
            else:
                entity_type = 'Commission Agent'

            db.session.commit()
            flash(f'SUCCESS: {form.entity.data} "{form.name.data}" Info with id "{id}" Updated', 'success')
            return redirect(url_for('display', active=active))

        except sqlalchemy.orm.exc.NoResultFound:
            flash(f"ERROR: A {entity_type} with this CNIC already exists!", "danger")
            return render_template('editbuyerandagent.html', entity=db_entity, form=form)
            

    else:     
        form.comments.data   = db_entity.person.comments

        if entity == 'Buyer':
            form.entity.data = 'Buyer'
        elif entity == 'Commission Agent':
            form.entity.data = 'Commission Agent'

        return render_template('editbuyerandagent.html', entity=db_entity, form=form)

    
def deletebuyer_(buyer):

    db.session.delete(buyer)
    db.session.commit()

    flash('Buyer Record Deleted!', 'danger')


def deleteagent_(agent):
    db.session.delete(agent)
    db.session.commit()

    flash('Agent Record Deleted!', 'danger')



def addexpenditure_(data):

    try: 
        type = Expenditure(
                    name=data['name']
                )
        db.session.add(type)
        db.session.commit()
        db.session.refresh(type)

        if data['flash']:
            flash(f'New Expenditure Type \'{type.name}\' Created', 'success')

        return type.id

    except IntegrityError as ie:
        flash(f'Expenditure Type \'{ data["name"] }\' Already Exists', 'danger')

   
def dealanalytics_(deal_id):

    deal        = Deal.query.filter_by(id=deal_id).first()
    transaction = Transaction.query.filter_by(deal_id=deal_id).order_by(Transaction.date_time).all()
    plot        = Plot.query.filter_by(id=deal.plot_id).first()

    if not transaction:
        return

    else:
        transaction_data = calc_transaction_analytics(deal_id, transaction, plot)
        return transaction_data


def addtransaction_(data):

    transaction = Transaction(
            amount         = data['amount'],
            date_time      = datetime.now(),
            comments       = data['comments'] or db.null(),
            deal_id        = ((data['type'] == 'deal') and data['id']) or db.null(),
            expenditure_id = ((data['type'] == 'ET')   and data['id']) or db.null()
        )

    db.session.add(transaction)
    db.session.commit()

    data['type'] == 'deal' and flash('Received Payment Successfuly Added to System', 'success')
    data['type'] == 'ET'   and flash('Expense Successfully Added to System'        , 'success')


def addexpense_(data):

    if data['name']:
        temp = addexpenditure_({'name': data['name'], 'flash': True})
        if temp is None:
            return 'duplicate'
        else:
            data['id'] = temp
    else:
        if data['id'] == 'None':
            flash('No Expenditure Type Selected', 'danger')
            return 'not selected'

    addtransaction_(data)


def add_user_or_employee_(data):

    #####  CURRENTLY NOT ADDING USER CNIC FILES, WILL DO IT LATER 


    #Adding user to the Database
    try:
        person = Person(
            name        = data['name'],
            cnic        = data['cnic'],
            phone       = data['phone'],
            email       = data['email'] if data['type'] == 1 else db.null(), 
            comments    = data['comments']            
        )
        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)

        user = User(
            password  = data['password'] if data['type'] == 1 else db.null(), 
            rank      = data['type'],
            person_id = person.id
        )
        db.session.add(user)
        db.session.commit()

        data['type'] == 1 and flash(f'User Successfully Added to the System'    , 'success')
        data['type'] == 2 and flash(f'Employee Successfully Added to the System', 'success')
        return

    except sqlalchemy.exc.IntegrityError as ie:
        if str(ie).find('person.email') > 0:
           flash(f"User with email {data['email']} already exists", 'danger')
        elif str(ie).find('person.cnic') > 0:
            flash(f"User with CNIC {data['cnic']} already exists", 'danger')
        elif str(ie).find('person.phone') > 0:
            flash(f"User with Phone Number {data['phone']} already exists", 'danger')
        return 'duplicate'


###------------------------REST ROUTES------------------------###

def filterplot_(status):

    plots = Plot.query.all() if status=='all' else Plot.query.filter_by(status=status).all()
    return jsonify(json_list=[plot.serialize for plot in plots])


def allbuyers_():

    return jsonify(json_list=[buyer.serialize for buyer in Buyer.query.all()])


def allplots_():

    return jsonify(json_list=[plot.serialize for plot in Plot.query.all()])


def alldeals_():

    return jsonify(json_list=[deal.serialize for deal in Deal.query.all()])


def allCAs_():

    return jsonify(json_list=[CA.serialize for CA in CommissionAgent.query.all()])


def allETs_():

    return jsonify(json_list=[ET.serialize for ET in Expenditure.query.all()])


def getIDfromTable_(table, id):

    exec(f"locals()['temp'] = {table}.query.filter_by(id={id}).first()")    
    return jsonify(json_list=[locals()['temp'].serialize])

###------------------------END REST ROUTES------------------------###

