from testing import Compound

# duration = 240
# loan_duration = "Months"
# interest_duration = "lump sum"



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
	    no_repay = 1/ 7
	    print("There are ", no_repay, "Week(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Weeks':
	    no_repay = 1
	    print("There are ", no_repay, "Week(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Months':
	    no_repay = 4
	    print("There are ", no_repay, "Month(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Years':
	    no_repay = 52

	    print("There are ", no_repay, "Year(s) in", duration, loan_duration)
	    return no_repay

def int_month(duration, interest_duration, loan_duration, interest):
	##### Months #######
	if interest_duration == 'Days':
	    no_repay = 1/30
	    print("There are ", no_repay, "Day(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Weeks':
	    no_repay = 1/4
	    print("There are ", no_repay, "Week(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Months':
	    no_repay = 1
	    print("There are ", no_repay, "Month(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Years':
	    no_repay = 12
	    print("There are ", no_repay, "Year(s) in", duration, loan_duration)
	    return no_repay

def int_year(duration, interest_duration, loan_duration):
	##### Years ######
	if interest_duration == 'Days':
	    no_repay = 1/360
	    print("There are ", no_repay, "Day(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Weeks':
	    no_repay = 1/52
	    print("There are ", no_repay, "Week(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Months':
	    no_repay = 1/12
	    print("There are ", no_repay, "Month(s) in", duration, loan_duration)
	    return no_repay
	elif interest_duration == 'Years':
	    no_repay = 1
	    print("There are ", no_repay, "Year(s) in", duration, loan_duration)
	    return no_repay


# no_repay = int(no_repay)
principal = int(input("Enter Your Principal:\n"))
interest = int(input("Enter Your Interest:\n"))
duration = int(input("Interest For:\n"))
loan_duration = input("Interest In:\n").capitalize()
interest_duration = input("Enter breakdown:\n").capitalize()


if loan_duration == "Days":
	gg = int_day(duration, interest_duration, loan_duration, interest)
	print("This is gg:",gg)
	compound_interest = Compound(principal, duration, interest_duration, loan_duration, interest, gg)
	print(compound_interest)
elif loan_duration == "Weeks":
	gg = int_week(duration, interest_duration, loan_duration, interest)
	print("This is gg:",gg)
	compound_interest = Compound(principal, duration, interest_duration, loan_duration, interest, gg)
	print(compound_interest)
elif loan_duration == "Months":
	gg = int_month(duration, interest_duration, loan_duration, interest)
	print("This is gg:",gg)
	compound_interest = Compound(principal, duration, interest_duration, loan_duration, interest, gg)
	print(compound_interest)
elif loan_duration == "Years":
	gg = int_year(duration, interest_duration, loan_duration, interest)
	print("This is gg:",gg)
	compound_interest = Compound(principal, duration, interest_duration, loan_duration, interest, gg)
	print(compound_interest)
else:
	print("Thank You")
