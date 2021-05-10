from flask      import current_app as app
from flask      import flash
from wtforms    import ValidationError
from statistics import mean

from .model     import *

from datetime   import datetime

import math
import re

def addperson(person_data):

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

def addfile(id, cnic, file, side):

    filename   = cnic + '_' + side

    file = File(    filename=filename,
                    format=file.filename.split('.')[-1],
                    data=file.read(),
                    person_id=id,
                )

    db.session.add(file)
    db.session.commit()


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


def get_cnic_file_data(id, cnic, data, fileformat, side, entity):


    cnic_file_data = { 'format'   : fileformat, 
                       'filename' : filename, 
                       'data'     : data, 
                       'person_id': id
                     }

    return cnic_file_data


def calc_transaction_analytics(deal_id, transaction, plot):

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