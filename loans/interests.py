from decimal import Decimal
from datetime import timedelta
import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from dateutil.relativedelta import relativedelta
import math


def int_day(duration, interest_duration, loan_duration, interest):
	if interest_duration == 'Days':
	    no_repay = 1
	    # print("There are ", no_repay, "Day(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Weeks':
	    no_repay = 7
	    # print("There are ", no_repay, "Week(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Months':
	    no_repay = 30
	    # print("There are ", no_repay, "Month(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Years':
	    no_repay = 360
	    # print("There are ", no_repay, "Day(s) in", duration, loan_duration)
	    return no_repay

def int_week(duration, interest_duration, loan_duration, interest):
	#### Weeks ######
	if interest_duration == 'Days':
	    no_repay = 1/7
	    return no_repay
	elif interest_duration == 'Weeks':
	    no_repay = 1
	    return no_repay
	elif interest_duration == 'Months':
	    no_repay = 4
	    return no_repay
	elif interest_duration == 'Years':
	    no_repay = 52
	    return no_repay

def int_month(duration, interest_duration, loan_duration, interest):
	##### Months #######
	if interest_duration == 'Days':
	    no_repay = 1/30
	    return no_repay
	elif interest_duration == 'Weeks':
	    no_repay = 1/4
	    return no_repay
	elif interest_duration == 'Months':
	    no_repay = 1
	    return no_repay
	elif interest_duration == 'Years':
	    no_repay = 12
	    return no_repay

def int_year(duration, interest_duration, loan_duration):
	##### Years ######
	if interest_duration == 'Days':
	    no_repay = 1/360
	    return no_repay
	elif interest_duration == 'Weeks':
	    no_repay = 1/52
	    return no_repay
	elif interest_duration == 'Months':
	    no_repay = 1/12
	    return no_repay
	elif interest_duration == 'Years':
	    no_repay = 1
	    return no_repay

# This is interest type calculator

def Flat_Rate(principal, interest, duration):
	flat_rate = (principal*duration*(interest/100))

	return flat_rate


def Equal_Principal(principal, duration, interest_duration, loan_duration, interest, period_principal, period):
	"""
	Total principal balance - Montly Principal Payment) x % interest
	"""
	equal_principal = (principal*interest)*float(period)
	# equal_principal = (((principal)-(period_principal))*(interest/100))*period
	# print("From Function::::", equal_principal)

	return equal_principal


def Interest_Only(principal, interest, duration):
	"""
	% interest x principal x duration
	"""
	interest = (principal*(interest/100))

	return interest

def Compound_Interest(principal, duration, interest_duration, loan_duration, interest, period):
	"""
	compound_interest = principal*(((1+(interest/100))**duration)-1)
	P [( 1 + %interestx1)^d -1)]
	5000*(((1+(5/100)*1)**10)-1)
	"""
	compound_interest = principal*(((1+(interest/100)*period)**duration)-1)
	
	return compound_interest


def Equal_Installments(principal, interest, duration):
	
	print("Reducing Balance - Equal Installments")


def get_payment_dates(loan_duration, cycle_duration, current_time, duration, payment_date):
	if loan_duration == 'Days' and cycle_duration == 'daily':
	    payment_date = current_time + relativedelta(days=duration)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'weekly':
	    payment_date = current_time + relativedelta(days=duration*7)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'biweekly':
	    payment_date = current_time + relativedelta(weeks=duration*2)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'monthly':
	    payment_date = current_time + relativedelta(months=duration)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'bimonthly':
	    payment_date = current_time + relativedelta(months=duration*2)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'quaterly':
	    payment_date = current_time + relativedelta(months=duration*4)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'every 4 months':
	    payment_date = current_time + relativedelta(months=duration*4)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'semi-annually':
	    payment_date = current_time + relativedelta(months=duration*6)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'yearly':
	    payment_date = current_time + relativedelta(years=duration*1)
	    return payment_date
	elif loan_duration == 'Days' and cycle_duration == 'lump sum':
	    payment_date = current_time + relativedelta(years=duration*7)
	    return payment_date
	#### Weeks #####
	elif loan_duration == 'Weeks' and cycle_duration == 'daily':
	    payment_date = current_time + relativedelta(days=duration)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'weekly':
	    payment_date = current_time + relativedelta(weeks=duration)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'biweekly':
	    payment_date = current_time + relativedelta(weeks=duration*2)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'monthly':
	    payment_date = current_time + relativedelta(weeks=duration*4)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'bimonthly':
	    payment_date = current_time + relativedelta(weeks=duration*8)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'quaterly':
	    payment_date = current_time + relativedelta(weeks=duration*12)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'every 4 months':
	    payment_date = current_time + relativedelta(months=duration*4)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'semi-annually':
	    payment_date = current_time + relativedelta(months=duration*8)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'yearly':
	    payment_date = current_time + relativedelta(years=duration)
	    return payment_date
	elif loan_duration == 'Weeks' and cycle_duration == 'lump sum':
	    payment_date = current_time + relativedelta(years=duration*4)
	    return payment_date

	##### Months #####
	elif loan_duration == 'Months' and cycle_duration == 'daily':
	    payment_date = current_time + relativedelta(days=duration*1)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'weekly':
	    payment_date = current_time + relativedelta(weeks=duration)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'biweekly':
	    payment_date = current_time + relativedelta(weeks=duration*2)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'monthly':
	    payment_date = current_time + relativedelta(months=duration)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'bimonthly':
	    payment_date = current_time + relativedelta(months=duration*2)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'quaterly':
	    payment_date = current_time + relativedelta(months=duration*3)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'every 4 months':
	    payment_date = current_time + relativedelta(months=duration*4)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'semi-annually':
	    payment_date = current_time + relativedelta(months=duration*6)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'yearly':
	    payment_date = current_time + relativedelta(months=duration*12)
	    return payment_date
	elif loan_duration == 'Months' and cycle_duration == 'lump sum':
	    payment_date = current_time + relativedelta(years=duration*12)
	    return payment_date

	##### Years #####
	elif loan_duration == 'Years' and cycle_duration == 'daily':
	    payment_date = current_time + relativedelta(days=duration)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'weekly':
	    payment_date = current_time + relativedelta(days=duration*4)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'biweekly':
	    payment_date = current_time + relativedelta(weeks=duration*2)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'monthly':
	    payment_date = current_time + relativedelta(months=duration)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'bimonthly':
	    payment_date = current_time + relativedelta(months=duration*2)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'quaterly':
	    payment_date = current_time + relativedelta(months=duration*3)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'every 4 months':
	    payment_date = current_time + relativedelta(months=duration*4)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'semi-annually':
	    payment_date = current_time + relativedelta(months=duration*6)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'yearly':
	    payment_date = current_time + relativedelta(months=duration*12)
	    return payment_date
	elif loan_duration == 'Years' and cycle_duration == 'lump sum':
	    payment_date = current_time + relativedelta(years=duration*360)
	    return payment_date
	else:
	    payment_date = current_time + relativedelta(years=duration)
	    return payment_date
