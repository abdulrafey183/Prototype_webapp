from flask              import flash, send_file, render_template, redirect, url_for, request, jsonify, abort
from flask              import current_app as app 
from flask_login        import login_user, current_user, logout_user
from flask_sqlalchemy   import sqlalchemy
from sqlalchemy.exc     import IntegrityError

# from .model             import *
from .utility           import *
from .forms             import *
from .middleware        import Middleware

from io         import  BytesIO
from datetime   import datetime

defualt_choice  = (None, 'Not Selected')


###------------------------START NORMAL ROUTES------------------------###
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
    # user_notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.date_time.desc()).limit(4)
    notices = Notes.query.order_by(Notes.date_time.desc()).all()[:10]
    return render_template('profile.html', current_user=current_user, notices=notices)


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


def analytics_():

    today = datetime.today()
    date_shortcuts = {
            1: today - datetime.timedelta(days=7),
            2: today - datetime.timedelta(days=14),
            3: today - datetime.timedelta(days=30),
            4: today - datetime.timedelta(days=90),
            5: today - datetime.timedelta(days=180),
            7: None,
        }

    form = AnalyticsForm()
    if form.validate_on_submit():

        if int(form.shortcuts.data) == 8:    #If Custom date range is selected
            start_date = str(form.start.data) + ' 00:00:00'
            end_date   = str(form.end.data)   + ' 23:59:59'

        else:
            start_date = date_shortcuts[int(form.shortcuts.data)]
            start_date = (start_date is not None and start_date.strftime('%Y-%m-%d') + ' 00:00:00') or start_date
            end_date   = today.strftime('%Y-%m-%d') + ' 23:59:59'

                
        expenses_title = (int(form.shortcuts.data)==7 and "All Time Expenses") or f'Expenses from {start_date[:-9]} to {end_date[:-9]}'
        revenue_title   = (int(form.shortcuts.data)==7 and "All Time Revenue")  or f'Revenues from {start_date[:-9]} to {end_date[:-9]}'

        total_expenses = str(expenses(start_date, end_date))
        total_revenue  = revenue(start_date, end_date)
        
        #expenses_pie_chart = get_expenses_chart(total_expenses)
        
        return render_template('analytics.html', 
                                form            = form, 
                                total_expenses  = total_expenses, 
                                expenses_title  = expenses_title,
                                total_revenue   = total_revenue,
                                revenue_title    = revenue_title
                              )

    return render_template('analytics.html', form=form)

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

###------------------------START ADD ROUTES------------------------###

def addbuyeroragent_():

    form = AddandEditBuyerorAgentForm()

    if form.validate_on_submit():

        try:
            entity = form.entity.data
            person_id = create_person(form)

            if entity == 'Buyer':
                active    = 'buyer'
                db_entity = Buyer(
                    address    = form.address.data,
                    person_id  = person_id                
                )

            elif entity == 'Commission Agent':
                active    = 'CA'
                db_entity = CommissionAgent(
                    person_id = person_id
                )

            db.session.add(db_entity)
            db.session.commit()

            # file1 = create_file(
            #         filename  = form.cnic.data + 'front',
            #         format    = form.cnic_front.filename.split('.')[-1],
            #         data      = form.cnic_front.data.read(),
            #         deal_id   = db.null(),
            #         person_id = person_id
            #     )

            # file2 = create_file(
            #         filename  = form.cnic.data + 'back',
            #         format    = form.cnic_back.filename.split('.')[-1],
            #         data      = form.cnic_back.data.read(),
            #         deal_id   = db.null(),
            #         person_id = person_id
            #     )

            ###---ADD FILES TO DATABASE---###

            if entity == 'Commission Agent':
                id = db_entity.person.id
            else:
                id = db_entity.id

            flash(f'SUCCESS: {entity} "{form.name.data}" added to record', 'success')
            return redirect(url_for('display', active=active))
        
        except IntegrityError as ie:
            
            ###---GENERATE RELEVANT ERROR MSG, WHICH FEILD IS DUPLICATE---###
            print(ie)
            ###------###s
            db.session.rollback()
            flash(f'ERROR: A {entity} with the entered credentials already exists!', 'danger')
    
    return render_template('addbuyerandagent.html',  form=form)


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

        buyer = Buyer.query.filter_by(id=form.buyer_id.data).first()
        plot  = Plot.query.filter_by(id=form.plot_id.data).first()
        CA    = CommissionAgent.query.filter_by(person_id=form.CA_id.data).first()

        if buyer is None:
            flash('No Buyer Selected', 'danger')
            return render_template('adddeal.html', form= form)
        elif plot is None:
            flash('No Plot Selected', 'danger')
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
            signing_date            = datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
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

            create_file(
                filename    = attachment.filename,
                format      = attachment.filename.split('.')[-1],
                data        = attachment.read(),
                deal_id     = deal.id,
                person_id   = db.null(),
                note_id     = db.null(),
            )
            # file = File(
            #     filename    = attachment.filename,
            #     format      = attachment.filename.split('.')[-1],
            #     data        = attachment.read(),
            #     deal_id     = deal.id,
            #     person_id   = db.null()
            # )
            # db.session.add(file)

        ###------REPLACE THIS WITH UTILITY FUCNTION------###
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


def addexpense_():

    ETs       = [(ET.id  , ET.name)            for ET   in Expenditure.query.all()         ]
    employees = [(user.id, user.person.name)   for user in User.query.filter(User.rank>0).all() ]
    deals     = [(deal.id, f"Deal# {deal.id}") for deal in Deal.query.filter(Deal.commission_agent_id).all()                ]
    
    ETs.insert      (0, defualt_choice)
    employees.insert(0, defualt_choice)
    deals.insert    (0, defualt_choice)

    form                    = AddExpenseForm()

    form.ET_id.choices      = ETs
    form.employee.choices   = employees
    form.deal.choices       = deals

    if form.validate_on_submit():

        data = {
            'type'        : 'ET',
            'name'        : form.ET_name.data,
            'id'          : (form.ET_id.data=='None'    and form.ET_id.data) or int(form.ET_id.data),
            'comments'    : form.comments.data,
            'amount'      : form.amount.data,
            'employee_id' : (form.employee.data!='None' and int(form.employee.data)) or None,
            'deal_id'     : (form.deal.data!='None'     and int(form.deal.data))     or None
        }
        
        if data['name']:
            temp = addexpendituretype_utility({'name': data['name'], 'flash': True})
            if temp is None:
                return render_template('addexpense.html', form=form, duplicateError=True)
            else:
                data['id'] = temp
        else:
            if data['id'] == 'None':
                flash('No Expenditure Type Selected', 'danger')
                return render_template('addexpense.html', form=form)

        #Checking if no employee is selected while paying salary
        if (data['id'] == 1) and (data['employee_id'] is None):
            flash('No Employee Selected', 'danger')
            return render_template('addexpense.html', form=form)

        #checking if no dea is selected while paying commission
        elif (data['id'] == 2) and (data['deal_id'] is None):
            flash('No Deal Selected', 'danger')
            return render_template('addexpense.html', form=form)

        addtransaction_utility(data)
        return redirect(url_for('profile'))

    return render_template('addexpense.html', form=form)


def add_user_or_employee_():


    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)

    form = AddUserOrEmployeeForm()
    form.name.label = 'Username'

    if form.validate_on_submit():

        data = {
            'type'      : int(form.type.data),
            'name'      : form.name.data,
            'email'     : form.email.data,
            'password'  : form.password.data or '12345',
            'cnic'      : form.cnic.data,
            'phone'     : form.phone.data,
            'cnic_front': form.cnic_front.data,
            'cnic_back' : form.cnic_back.data,
            'comments'  : form.comments.data or db.null()
        }

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

            #Adding CNIC Front file to the database
            if form.cnic_front.data:
                create_file(
                        filename  = data['name'] + "_cnic_front." + data['cnic_back'].filename.split('.')[-1],
                        format    = data['cnic_front'].filename.split('.')[-1],
                        data      = data['cnic_front'].read(),
                        deal_id   = db.null(),
                        person_id = person.id
                    )

            #Adding CNIC Back file to the database
            if form.cnic_front.data:
                create_file(
                        filename  = data['name'] + "_cnic_back." + data['cnic_back'].filename.split('.')[-1],
                        format    = data['cnic_back'].filename.split('.')[-1],
                        data      = data['cnic_back'].read(),
                        deal_id   = db.null(),
                        person_id = person.id
                    )

            #Displaying Success Flash Message
            data['type'] == 1 and flash(f'User Successfully Added to the System'    , 'success')
            data['type'] == 2 and flash(f'Employee Successfully Added to the System', 'success')
            return redirect(url_for('profile'))

        except IntegrityError as ie:
            if str(ie).find('person.email') > 0:
               flash(f"User with email {data['email']} already exists", 'danger')
            elif str(ie).find('person.cnic') > 0:
                flash(f"User with CNIC {data['cnic']} already exists", 'danger')
            elif str(ie).find('person.phone') > 0:
                flash(f"User with Phone Number {data['phone']} already exists", 'danger')

    return render_template('add-user-or-employee.html', form=form)


def receivepayment_(id):

    try:   
         
        deal  = Deal.query.get(id)
        form   = ReceivePaymentForm(deal_id=deal.id)
        form.deal_id.choices = [(row[0], "DEAL# " + str(row[0])) for row in Deal.query.with_entities(Deal.id).all()]       
           
    except AttributeError as ae:
        abort(404)

    if form.validate_on_submit():
        data = {
            'type': 'deal',
            'id'  : form.deal_id.data,
            'comments': form.comments.data,
            'amount': form.amount.data
        }
        addtransaction_utility(data)

        return redirect(url_for('profile'))        

    return render_template('receivepayment.html', form=form)


def addnotes_():

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
        db.session.refresh(note)

        # Adding Notice Attachments to the Database
        for attachment in form.attachments.data:

            create_file(
                filename    = attachment.filename, 
                format      = attachment.filename.split('.')[-1], 
                data        = attachment.read(), 
                deal_id     = db.null(), 
                person_id   = db.null(), 
                note_id     = note.id
            )

            # file = File(
            #     filename    = attachment.filename,
            #     format      = attachment.filename.split('.')[-1],
            #     data        = attachment.read(),
            #     deal_id     = db.null(),
            #     person_id   = db.null(),
            #     note_id     = note.id
            # )
            # db.session.add(file)

        flash(f'Note Added!', 'success')
        return redirect(url_for('profile'))


    return render_template('addnotes.html', form=form)


def addexpendituretype_():

    form = AddExpendituretypeForm()
    if form.validate_on_submit():
        data = {
            'name'  : form.name.data,
            'flash' : True 
        }
        if addexpendituretype_utility(data) is not None: 
            return redirect(url_for('display', active="ET"))

    return render_template('addexpendituretype.html', form=form)


###------------------------END ADD ROUTES------------------------###



###------------------------START INFO ROUTES------------------------###

def noteinfo_(note_id):
    
    notice = Notes.query.filter_by(id=note_id).first()

    if notice is None:
        flash(f'No such notice exists!', 'danger')
        return redirect(url_for('profile'))

    # if note.user_id != current_user.id:
    #     abort(403)

    return render_template('noteinfo.html', note=notice, current_user=current_user)


def buyerinfo_(buyer_id):
    buyerinfo = True
    buyer     = Buyer.query.filter_by(id=int(buyer_id) ).first()

    if buyer is None:
        flash('ERROR: NO Such buyer exists', 'danger')
        
    return render_template('agentandbuyerinfo.html', entity=buyer, buyerinfo=buyerinfo)

def agentinfo_(agent_id):
    agentinfo = True
    agent     = CommissionAgent.query.filter_by(person_id=int(agent_id)).first()

    if agent is None:
        flash('ERROR: NO Such agent exists', 'danger')
        
    return render_template('agentandbuyerinfo.html', entity=agent, agentinfo=agentinfo)

def plotinfo_(plot_id):
    plot = Plot.query.get(int(plot_id))
    if plot is None:
        flash('No Such plot exists', 'danger')
        return redirect(url_for('display', active='plot'))
        
    return render_template('plotinfo.html', plot=plot)


def dealinfo_(deal_id):

    deal = Deal.query.filter_by(id=deal_id).first()
    if deal is None:
        flash('ERROR: NO Such deal exists', 'danger')
        return redirect(url_for('display', active='deal'))

    plot        = Plot.query.filter_by(id=deal.plot_id).first()
    transaction = Transaction.query.filter_by(deal_id=deal_id).order_by(Transaction.date_time).all()

    total_commission      = len(deal.commissions)
    total_commission_paid = sum([commission.transaction.amount for commission in deal.commissions])
    
    transaction_data = (len(transaction) and calc_deal_transaction_data(deal_id, transaction, plot)) or None
    
    return render_template('dealinfo.html', 
                            deal                    = deal,
                            transaction             = transaction_data, 
                            total_commission        = total_commission, 
                            total_commission_paid   = total_commission_paid
                          )


def expenditureinfo_(expenditure_id):

    expenditure = Expenditure.query.filter_by(id=expenditure_id).first()
    if expenditure is None:
        flash('ERROR: NO Such expenditure exists', 'danger')
        return redirect(url_for('display', active='expenditure'))

    transaction = Transaction.query.filter_by(expenditure_id=expenditure_id).order_by(Transaction.date_time).all()
    print(transaction)
    if not transaction:
        transaction_data = None
        #return render_template('expenditureinfo.html', expenditure=expenditure, transaction=transaction_data)
    else:
        transaction_data = calc_expense_transaction_data(expenditure_id, transaction)
        
    return render_template('expenditureinfo.html', expenditure=expenditure, transaction=transaction_data)


def employeeinfo_(employee_id):
    employee      = User.query.get(int(employee_id))

    if employee is None:
        flash('No Such Employee exists', 'danger')
        return redirect(url_for('display', active='employee'))

    total_salaries = len(employee.salaries) and sum(salary.transaction.amount for salary in employee.salaries)
    transactions   = [salary.transaction for salary in employee.salaries]
    print(transactions)
    return render_template('employeeinfo.html', employee=employee, total_salaries=len(employee.salaries), total_salaries_amount=total_salaries, transactions=transactions)


###------------------------END INFO ROUTES------------------------###
    


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
    return redirect(url_for('display', active='buyer'))


def deleteagent_(agent):

    #Checking Authorization
    Middleware.authorizeSuperUser(current_user)

    agent = CommissionAgent.query.filter_by(person_id=agent_id).first()

    # if no record of buyer with entered id is found
    if agent is None:
        flash(f'No such agent exists!', 'danger')
        return redirect(url_for('display', active='CA'))

    db.session.delete(agent)
    db.session.commit()

    flash('Agent Record Deleted!', 'danger')
    return redirect(url_for('display'))


###------------------------START REST ROUTES------------------------###

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


def allEmployees_():

    return jsonify(json_list=[user.serialize for user in User.query.filter(User.rank>0).all()])



def getIDfromTable_(table, id):

    exec(f"locals()['temp'] = {table}.query.filter_by(id={id}).first()")    
    return jsonify(json_list=[locals()['temp'].serialize])

###------------------------END REST ROUTES------------------------###

