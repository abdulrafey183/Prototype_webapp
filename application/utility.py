from flask              import current_app as app
from flask              import flash
from wtforms            import ValidationError
from sqlalchemy.exc     import IntegrityError
from sqlalchemy.orm     import session
from sqlalchemy         import func

from .model     import *

from datetime   import datetime
from statistics import mean
from matplotlib import pyplot as plt
from io         import  BytesIO

import math
import re
import base64



def create_person(person_data):
    """
    Utility Function that adds a row to the Person Table and returns the 
    primary key of that row
    """

    person = Person(
                name    = person_data.name.data,
                cnic    = person_data.cnic.data,
                phone   = person_data.phone.data,
                email   = person_data.email.data,
                comments= person_data.comments.data if person_data.comments.data else db.null()
            )

    db.session.add(person)
    db.session.commit()

    return person.id


    """
    Utility Function that adds a row to the File Table and returns the 
    primary key of that row
    """
def create_file(filename, format, data, deal_id, person_id):

    file = File(    
            filename    = filename,
            #format      = file.filename.split('.')[-1],
            format      = format,
            #data        = file.read(),
            data        = data,
            deal_id     = deal_id,
            person_id   = person_id,
           )

    db.session.add(file)
    db.session.commit()
    db.session.refresh(file)

    return file.id


def create_transaction(amount, comments, deal_id, expenditure_id):
    """
    Utility Function that adds a row to the Transaction Table and returns the 
    primary key of that row
    """

    transaction = Transaction(
            amount         = amount,
            date_time      = datetime.now(),
            comments       = comments,
            deal_id        = deal_id,
            expenditure_id = expenditure_id
    )

    db.session.add(transaction)
    db.session.commit()
    db.session.refresh(transaction)

    return transaction.id


def create_salary(employee_id, transaction_id):
    """
    Utility Function that adds a row to the Salary Table and returns the 
    primary key of that row
    """

    salary = Salary(
        employee_id    = employee_id,
        transaction_id = transaction_id
    )

    db.session.add(salary)
    db.session.commit()
    db.session.refresh(salary)

    return salary.id


def create_commission(commission_agent_id, transaction_id):
    """
    Utility Function that adds a row to the commission Table and returns the 
    primary key of that row
    """

    commission = Commission(
        commission_agent_id = commission_agent_id,
        transaction_id      = transaction_id
    )

    db.session.add(commission)
    db.session.commit()
    db.session.refresh(commission)

    return commission.id


def addtransaction_utility(data):

    transaction_id = create_transaction(
        data['amount'],
        data['comments'] or db.null(),
        ((data['type'] == 'deal') and data['id']) or db.null(),
        ((data['type'] == 'ET')   and data['id']) or db.null()
    )


    #If transaction is a Salary
    if (data['type'] == 'ET') and data['employee_id']:
        create_salary(data['employee_id'], transaction_id)
        
    #If transaction is a Commission
    elif (data['type'] == 'ET') and data['deal_id']:
        CA_id = Deal.query.get(data['deal_id']).commissionagent.person_id
        create_commission(CA_id, transaction_id)        


    data['type'] == 'deal' and flash('Received Payment Successfuly Added to System', 'success')
    data['type'] == 'ET'   and flash('Expense Successfully Added to System'        , 'success')


def addexpendituretype_utility(data):

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



def get_cnic_file_data(id, cnic, data, fileformat, side, entity):


    cnic_file_data = { 'format'   : fileformat, 
                       'filename' : filename, 
                       'data'     : data, 
                       'person_id': id
                     }

    return cnic_file_data


def calc_deal_transaction_data(deal_id, transaction, plot):

    no_of_installments   = len(transaction)    # total number of transactios made
    avg_installment_freq = calc_avg_installment_freq(transaction)    # average time between each transaction
    
    amount_paid          = sum(t.amount for t in transaction)        # total amount paid in all transactions
    amount_left          = plot.price - amount_paid                  # the total amount left to be paid
    avg_amount_paid      = math.ceil(mean([t.amount for t in transaction]))     # average amount paid per installment

    installment_left     = math.ceil(amount_left // avg_amount_paid)  # expected number of installments left 
    predicted_amount     = math.ceil(amount_left // installment_left) # predicted amount paid for the next installments left
    expected_time_left   = calc_expected_time_left(avg_installment_freq, installment_left)

    transaction_data = {    "deal_id"              : deal_id,
                            "transactions"         : transaction,
                            "total_installments"   : no_of_installments,
                            "avg_installment_freq" : avg_installment_freq, 
                            "amount_paid"          : amount_paid,
                            "amount_left"          : amount_left,
                            "avg_amount_paid"      : avg_amount_paid,
                            "predicted_amount"     : predicted_amount,
                            "installment_left"     : installment_left,
                            "expected_time_left"   : expected_time_left
                        }

    return transaction_data


def calc_expense_transaction_data(expenditure_id, transaction):

    no_of_transactions = len(transaction)
    total_amount       = sum(t.amount for t in transaction)

    expense_data = { 
                        "no_of_transactions" : no_of_transactions,
                        "total_amount"       : total_amount,
                        "transactions"        : transaction
                   }

    return expense_data




def calc_expected_time_left(avg_installment_freq, installment_left):

    if avg_installment_freq: 
        # expected time for the payments to complete
        expected_time_left   = str(int(avg_installment_freq.split()[0]) * installment_left) + " " + " ".join(avg_installment_freq.split()[1:]) 
    else:
        expected_time_left = None

    return expected_time_left


def calc_avg_installment_freq(transaction):

    installment_freq     = [(j.date_time - i.date_time).days for i, j in zip(transaction[:-1], transaction[1:])]

    if not installment_freq:
        return

    avg_installment_freq = math.ceil(mean(installment_freq))

    if avg_installment_freq > 0:
        return str(avg_installment_freq) + " Day(s)"
    else:
        return calc_time_in_hours(transaction)


def calc_time_in_hours(transaction):

    installment_freq     = [((j.date_time - i.date_time).seconds)//3600 for i, j in zip(transaction[:-1], transaction[1:])]

    avg_installment_freq = math.ceil(mean(installment_freq))

    if avg_installment_freq > 0:
        return str(avg_installment_freq) + " Hours"
    else:
        return calc_time_in_minutes(transaction)


def calc_time_in_minutes(transaction):

    installment_freq     = [((j.date_time - i.date_time).seconds)//60%60 for i, j in zip(transaction[:-1], transaction[1:])]

    avg_installment_freq = math.ceil(mean(installment_freq))

    return str(avg_installment_freq) + " Minutes"


### Custom Form Validators ###

# validate phone and cnic
def validate_phone_and_cnic(form, field):
    if not re.match(r'^([\s\d]+)$', field.data):
        raise ValidationError('Enter Numbers Only!')



###-------------START ANALYTICS FUCNTIONS-------------###

def aggregate(start= None, end= None):
    
    # will throw an error if table is empty
    start = start or db.session.query(func.min(Transaction.date_time)).one()[0] # if no start date provided, selecting oldest date in table
    end   = end   or datetime.now()                                    # if no end date provided, selecting today's date

    return db.session                      \
        .query(
            Transaction.date_time,
            func.sum(Transaction.amount)
        )                                   \
        .filter(
            Transaction.date_time >= start,
            Transaction.date_time <= end,
        )               


def revenue(start= None, end= None):

    res = aggregate(start, end)                     \
        .filter(Transaction.deal_id != db.null()) \
        .group_by(Transaction.date_time)            \
        .all()


def expenses(start= None, end= None):

    # res = aggregate(start, end)                     \
    #     .filter(Transaction.expenditure_id != db.null()) \
    #     .group_by(Transaction.date_time)            \
    #     .all()    

    res = db.session                      \
        .query(
            Transaction.expenditure_id,
            func.sum(Transaction.amount)
        ).filter(
            Transaction.date_time >= start,
            Transaction.date_time <= end,
            Transaction.expenditure_id != db.null()
        ).group_by(
            Transaction.expenditure_id
        ).all()

    return res and { Expenditure.query.get(id).name: int(amount) for (id, amount) in res}


def net_profits(): pass

###-------------END ANALYTICS FUCNTIONS-------------###


###-------------START PLOTTING FUNCTIONS-------------###

def get_expenses_chart(expenses):

    plt.pie(expenses.values(), labels=expenses.keys())
        
    graph_IObytes = BytesIO()
    plt.savefig(graph_IObytes, format='jpg')
    graph_IObytes.seek(0)

    return str(base64.b64encode(graph_IObytes.read()))[2:-1]

