from flask import current_app as app
from statistics import mean
import math
import re

def savecnic(cnicfile, cnic, side):

    ''' 
    Utility function to save the CNIC image file
    uploaded by the user.
    '''
    
    if not cnicfile:
        flash("ERROR: CNIC Image Missing!", "danger")
        return False

    # path to folder for storing cnic images
    cnic_file_path = app.root_path + '\\static\\img\\cnic\\agents\\' + str(cnic) + side + '.jpg'

    cnicfile.save(cnic_file_path)
    return cnic_file_path


def calc_transaction_analytics(deal_id, transaction, plot):

    no_of_installments   = len(transaction)                          # total number of transactios made
    avg_installment_freq = calc_avg_installment_freq(transaction)    # average time between each transaction
    
    amount_paid          = sum(t.amount for t in transaction)        # total amount paid in all transactions
    amount_left          = plot.price - amount_paid                  # the total amount left to be paid
    avg_amount_paid      = math.ceil(mean([t.amount for t in transaction]))     # average amount paid per installment

    installment_left     = math.ceil(amount_left // avg_amount_paid)  # expected number of installments left 
    predicted_amount     = math.ceil(amount_left // installment_left) # predicted amount paid for the next installments left

    # expected time for the payments to complete
    expected_time_left   = str(int(avg_installment_freq.split()[0]) * installment_left) + " " + " ".join(avg_installment_freq.split()[1:])

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

def calc_avg_installment_freq(transaction):

    installment_freq     = [(j.date_time - i.date_time).days for i, j in zip(transaction[:-1], transaction[1:])]
    avg_installment_freq = mean([days for days in installment_freq])
    
    if avg_installment_freq == 0:
        return

    elif avg_installment_freq < 30:
        return str(avg_installment_freq) + " Day(s)"

    elif avg_installment_freq >= 30:
        return str(avg_installment_freq//30) + " Month(s)"

    else:
        return

### Custom Form Validators ###

# validate phone and cnic
def validate_phone_and_cnic(form, field):
    if not re.match(r'^([\s\d]+)$', field.data):
        raise ValidationError('Enter Numbers Only!')