from flask      import current_app as app
from flask      import flash
from wtforms    import ValidationError
from statistics import mean

import math
import re

def get_cnic_file_data(id, cnic, data, fileformat, side, entity):

    filename   = cnic + '_' + side

    cnic_file_data = { 'cnic'     : True, 
                       'format'   : fileformat, 
                       'filename' : filename, 
                       'data'     : data, 
                     }
    if entity == 'Buyer':
        cnic_file_data.update({'agent_id' : False, 'buyer_id' : id})
    if entity == 'Commission Agent':
        cnic_file_data.update({'agent_id' : id, 'buyer_id' : False})

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