from flask              import flash
from flask              import current_app as app
from flask_login        import login_user
from flask_sqlalchemy   import sqlalchemy
from sqlalchemy.exc     import IntegrityError

from .model   import *
from .utility import *

from datetime import datetime


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


### Buyer ###
def addbuyer_(buyer_data):
    try:

        front = savecnic(buyer_data.cnic_front.data, buyer_data.cnic.data, 'front')
        back  = savecnic(buyer_data.cnic_back.data, buyer_data.cnic.data, 'back')

        if not front or not back:
            return False

        buyer = Buyer(
            name       = buyer_data.name.data,
            cnic       = buyer_data.cnic.data,
            phone      = buyer_data.phone.data,
            email      = buyer_data.email.data,
            address    = buyer_data.address.data,
            cnic_front = front,
            cnic_back  = back,
            comments   = buyer_data.comments.data if buyer_data.comments.data else db.null()
        )

        db.session.add(buyer)
        db.session.commit()

        flash(f'Buyer with id "{buyer.id}" created', 'success')
        return True

    except sqlalchemy.exc.IntegrityError:
        flash('ERROR: A buyer with this CNIC already exists!', 'danger')
        return False


def editbuyer_(buyer_id, buyer_data):

    try:
        db.session.query(Buyer).filter_by(
            id=buyer_id
        ).update({
            'name': buyer_data.name.data,
            'cnic': buyer_data.cnic.data,
            'phone': buyer_data.phone.data,
            'email': buyer_data.email.data,
            'address': buyer_data.address.data,
            'comments': buyer_data.comments.data if buyer_data.comments.data else db.null()
        })
        db.session.commit()
        flash(f'Buyer Info with id "{buyer_id}" Updated', 'success')
        return True

    except sqlalchemy.orm.exc.NoResultFound:
        flash("ERROR: A buyer with this CNIC already exists!", "danger")
        return False


def deletebuyer_(buyer):

    db.session.delete(buyer)
    db.session.commit()

    flash('Buyer Record Deleted!', 'danger')

### Commission Agent ###
def addagent_(agent_data):
    try:

        front = savecnic(agent_data.cnic_front.data, agent_data.cnic.data, 'front')
        back  = savecnic(agent_data.cnic_back.data, agent_data.cnic.data, 'back')

        if not front or not back:
            return False

        agent = CommissionAgent(
            name       = agent_data.name.data,
            cnic       = agent_data.cnic.data,
            phone      = agent_data.phone.data,
            email      = agent_data.email.data,
            cnic_front = front,
            cnic_back  = back,
            comments   = agent_data.comments.data if agent_data.comments.data else db.null()
        )

        db.session.add(agent)
        db.session.commit()

        flash(f'Agent with id "{agent.id}" created', 'success')
        return True

    except sqlalchemy.exc.IntegrityError:
        flash('ERROR: An Agent with this CNIC already exists!', 'danger')
        return False


def editagent_(agent_id, agent_data):

    try:
        db.session.query(CommissionAgent).filter_by(
                            id=agent_id
                            ).update({ 
                                'name'     : agent_data.name.data,
                                'cnic'     : agent_data.cnic.data,
                                'phone'    : agent_data.phone.data,
                                'email'    : agent_data.email.data,
                                'comments' : agent_data.comments.data if agent_data.comments.data else db.null()
        })

        db.session.commit()
        flash(f"Agent Info with id '{agent_id}' Updated", 'success')
        return True

    except sqlalchemy.orm.exc.NoResultFound:
        flash("ERROR: A agent with this CNIC already exists!", "danger")
        return False


def deleteagent_(agent):
    db.session.delete(agent)
    db.session.commit()

    flash('Agent Record Deleted!', 'danger')

def adddeal_(deal_data):

    plot = Plot.query.filter_by(id=deal_data['plot_id']).first()
    buyer = Buyer.query.filter_by(id=deal_data['buyer_id']).first()
    CA = CommissionAgent.query.filter_by(id=deal_data['CA_id']).first()

    if plot is None:
        flash('No Plot Selected', 'danger')
        return 'plot error'
    elif buyer is None:
        flash('No Buyer Selected', 'danger')
        return 'buyer error'

    print(
        f"------------------------\nPLOT ID: {plot}\nBUYER ID: {buyer}\nCA ID: {CA}\n------------------------")

    # Setting the plot price according to the price provided by user
    db.session.query(Plot).filter_by(id=deal_data['plot_id']).update(
        {'price': deal_data['plot_price']})
    db.session.commit()
    db.session.refresh(plot)

    # UPDATING CORESPONDING PLOT AND DEAL STATUS
    if (deal_data['first_amount_recieved'] == plot.price):
        plot.status = 'sold'
        deal_status = 'completed'
    else:
        plot.status = 'in a deal'
        deal_status = 'on going'

    db.session.add(plot)

    print(plot.status, deal_status)

    # Creating Deal and adding to Database
    deal = Deal(
        status=deal_status,
        signing_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        amount_per_installment=deal_data['amount_per_installment'] if deal_data['amount_per_installment'] else db.null(
        ),
        installment_frequency=deal_data['installment_frequency'] if deal_data['installment_frequency'] else db.null(
        ),
        commission_rate=deal_data['c_rate'] if deal_data['c_rate'] else db.null(
        ),
        comments=deal_data['comments'] if deal_data['comments'] else db.null(),
        buyer_id=deal_data['buyer_id'],
        plot_id=deal_data['plot_id'],
        commission_agent_id=CA.id if CA else db.null(),
    )

    db.session.add(deal)
    db.session.commit()
    db.session.refresh(deal)

    # Adding Deal Attachments to the Database
    for attachment in deal_data['attachments']:
        file = File(
            format=attachment.filename.split('.')[-1],
            data=attachment.read(),
            deal_id=deal.id,
            buyer_id=db.null()
        )
        db.session.add(file)

    # Creating corresponding transaction and adding to Database
    transaction = Transaction(
        amount=deal_data['first_amount_recieved'],
        date_time=datetime.now(),
        comments=f'Initial Transaction for Deal {deal.id}',
        deal_id=deal.id,
        expenditure_id=db.null()
    )

    db.session.add(transaction)
    db.session.commit()

    flash(f'Deal with ID {deal.id} successfully created!', 'success')


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
            deal_id        = data['id'] if data['type'] == 'deal' else db.null(),
            expenditure_id = data['id'] if data['type'] == 'ET'   else db.null()
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
            # addtransaction_(data)
    else:
        if data['id'] == 'None':
            flash('No Expenditure Type Selected', 'danger')
            return 'not selected'
        # else:
        #     addtransaction_(data)

    addtransaction_(data)
    

    
        

    

