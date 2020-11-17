import calendar
import json
import requests
import hashlib
import datetime
import random
import decimal
from decimal import Decimal
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FileUploadParser
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
from .serializers import *
from .models import *
from accounts.models import (
	Profile
)
from borrowers.models import *
from borrowers.serializers import BorrowerSerializer
from .utils import details_from_bvn, compare_dates, get_loan_score, get_account_name
from .save_auth_code import ddebitCode
from .direct_debit import directDebit
from .interests import *
from loan_management_system import settings, urls

today = datetime.date.today()

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])


class LoanView(APIView):

	def post(self, request):
		check_branch = Branch.objects.filter(id=request.data['branch']).exists()
		if check_branch:
			get_branch = Branch.objects.get(id=request.data['branch'])
		else:
			return Response({"Error": "Branch ID does not exists"}, status=status.HTTP_400_BAD_REQUEST)
		if get_branch.is_open == False:
			return Response({"Error": "Selected Branch is not opened yet. Choose another branch for this loan."}, status=status.HTTP_400_BAD_REQUEST)
		# initialize a loan by customer
		serializer = LoanSerializer2(data=request.data)
		
		if serializer.is_valid():
			serializer.save()
			obj = serializer.save()
			res = serializer.data
			get_bor = Borrower.objects.get(id=res['borrower'])
			get_loan_officer = LoanOfficer.objects.get(id=get_bor.loan_officer.id)
			OfficerLoan.objects.create(loan=obj, loan_officer=get_loan_officer)
			# Return Back the loan ID that was created...
			the_loan = Loan.objects.get(id=obj.id)
			loan_interest_percentage = float(the_loan.loan_interest_percentage)
			principal_amount = float(the_loan.principal_amount)
			no_of_repayments = int(the_loan.no_of_repayments)
			interest_method = the_loan.interest_method
			loan_duration_period = the_loan.loan_duration_period
			repayment_cycles = the_loan.repayment_cycles
			duration = int(the_loan.duration)
			interest_rate = float(the_loan.loan_interest_percentage)
			loan_interest_percentage_period = the_loan.loan_interest_percentage_period

			interest = float(loan_interest_percentage)/100
			loan_interest = float(principal_amount)*interest
			principal_payment = round(float(principal_amount)/float(no_of_repayments), 2)
			current_time = today
			payment_date = current_time
			try:
				existing_schedules = LoanScheduler.objects.filter(loan = the_loan).delete()
			except:
				pass

			if interest_method == 'Flat Rate':
				repayment_amount = round((loan_interest)+(principal_payment), 2)
				flat_rate = Flat_Rate(principal_amount, loan_interest_percentage, no_of_repayments)
				loan_repayment_amount = flat_rate+principal_amount
				
				for duration in range(1, int(no_of_repayments) + 1):
					payment_dates = get_payment_dates(loan_duration_period, repayment_cycles, current_time, duration, payment_date)

					off_principal = round((principal_amount)/(no_of_repayments), 2)
					off_interest = round((flat_rate)/(no_of_repayments), 2)
					total_due = round(float(off_principal)+float(off_interest), 2)
					off_paid = 0.00
					d_due = round((principal_amount)/(no_of_repayments), 2)
					d_due2 = round((flat_rate)/(no_of_repayments), 2)
					d_due3 = round((d_due)+(d_due2), 2)
					new_payment = float(off_principal)+float(off_interest)
					pending_due = float(total_due)-float(the_loan.amount_paid)
					principal_payment -= float(principal_amount/no_of_repayments)
					principal_payment = round((principal_payment) + float(principal_amount/no_of_repayments), 2)
					total_due_amount = round(d_due3 * no_of_repayments, 2)

					my_fee = 0

					loan_fees = the_loan.loan_fees.all()
					for fees in loan_fees:
						my_fee += fees.amount

					loan_scheduler = LoanScheduler.objects.create(
						loan=the_loan,
						description = "Repayment",
						date=payment_dates,
						principal = off_principal,
						interest = off_interest,
						fees = round(my_fee/the_loan.no_of_repayments, 2),
						penalty = round(the_loan.penalty_amount/the_loan.no_of_repayments, 2),
						due = d_due3,
						paid = 0.00,
						principal_paid = 0.00,
						pending_due = round(pending_due, 2),
						total_due = round(total_due, 2),
						principal_due = off_principal,
						amount=principal_payment,
						status='pending'
					)

				the_loan.interest_rate = Decimal(the_loan.interest_rate)
				the_loan.interest_rate = Decimal(the_loan.interest_rate)
				loan_interest += (interest_rate/100) * principal_amount
				the_loan.interest = Decimal(flat_rate)
				the_loan.total_due_principal = principal_amount
				the_loan.total_due_interest = loan_repayment_amount
				the_loan.total_due_fees = the_loan.loan_fees
				the_loan.total_due_penalty = the_loan.penalty_amount
				the_loan.loan_release_date = current_time
				the_loan.remaining_balance = loan_repayment_amount
				the_loan.repayment_amount = loan_repayment_amount

				the_loan.save()
				loan_schedules = LoanScheduler.objects.filter(loan = the_loan)
				last_loan_schedules = LoanScheduler.objects.filter(loan = the_loan).last()
				next_loan_payment = LoanScheduler.objects.filter(loan=the_loan).filter(status='pending').first()
				Loan.objects.filter(id=the_loan.id).update(maturity_date=last_loan_schedules.date, current_repayment_amount=next_loan_payment.due)
				serializer = LoanSchedulerSerializer(loan_schedules, many=True)

				# Get the id of current loansReducing Balance - Equal Principal
				# loans = Loan.objects.all()
				# max_acc_no = loans.aggregate(Max('account_no'))
				# max_acc_id = max_acc_no['account_no__max']
				# max_acc_no_int = int(max_acc_id)
				# max_acc_no_add = max_acc_no_int + 1
				# # Lets update the account no with this one.
				# Loan.objects.filter(id=res['id']).update(account_no=max_acc_no_add)
				# return Response({"message": "loan has been created...", "schedules":serializer.data}, status=status.HTTP_201_CREATED)
				return Response({"message": res}, status=status.HTTP_201_CREATED)
			# save loan and send loan application email.
			#serializer.save()
			#res = serializer.data
			#return Response(res, status=status.HTTP_200_OK)
		#return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

			elif interest_method == 'Reducing Balance - Equal Principal':
				if loan_duration_period == "Days":
					period = int_day(duration, loan_interest_percentage_period, loan_duration_period, interest)
					equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)
				elif loan_duration_period == "Weeks":
					period = int_week(duration, loan_interest_percentage_period, loan_duration_period, interest)
					equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)
				elif loan_duration_period == "Months":
					period = int_month(duration, loan_interest_percentage_period, loan_duration_period, interest)
					equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)
				elif loan_duration_period == "Years":
					period = int_year(duration, loan_interest_percentage_period, loan_duration_period, interest)
					equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)

				equal_principal = round(equal_principal, 2)
				interest_schedule = equal_principal/no_of_repayments
				principal_due = principal_amount/no_of_repayments

				pend_due = float(principal_amount)/float(no_of_repayments)
				pend_due = pend_due+float(equal_principal)
				principal_plus_interest = 0.0
				total_interest = 0
				amount = principal_amount
				total_loan_fees = 0.0
				total_repayment_amount_per_schedule = principal_amount / no_of_repayments

				for duration in range(1, int(no_of_repayments) + 1):
					payment_dates = get_payment_dates(loan_duration_period, repayment_cycles, current_time, duration, payment_date)
					repayment_schedule = principal_due + (principal_amount * (interest_rate / 100))
					principal_plus_interest += repayment_schedule

					due = float(principal_amount)/float(no_of_repayments)
					due = due+float(equal_principal)

					equal_principal -= round(interest_schedule, 2)
					reducing_interest = equal_principal+interest_schedule

					principal_schedule = principal_amount/no_of_repayments
					increasing_principal = principal_schedule - principal_due
					principal_amt = principal_amount/no_of_repayments
					amount -= principal_amt
					increasing_principal = round((amount) + float(principal_schedule), 2)


					pen_due = (float(principal_amount)/float(no_of_repayments)) + float(equal_principal)
					pend_due += float(due) - float(interest_schedule)
					pending_due = (pend_due - pen_due)
					total_due = (pend_due - pen_due)

					loan_scheduler = LoanScheduler.objects.create(
						loan=the_loan,
						description = "Repayment",
						date=payment_dates,
						principal = round(Decimal(principal_amount)/Decimal(no_of_repayments), 2),
						interest = round(reducing_interest, 2),
						fees = total_loan_fees/no_of_repayments,
						penalty = 0.00,
						due=round(due, 2),
						paid = 0.00,
						pending_due = round(pending_due, 2),
						total_due = total_due,
						principal_due = round(increasing_principal, 2),
						amount = round(increasing_principal, 2),
						# Principal Outstanding - Principal Due [for each cycle] (Reducing),
						status='pending'
						)
					principal_amount -= total_repayment_amount_per_schedule
					loan_fees = the_loan.loan_fees.all()
					total_loan_fee = 0.0
					the_loan.interest = equal_principal
				the_loan.total_due_principal = round((the_loan.principal_amount)/(the_loan.no_of_repayments) * (the_loan.no_of_repayments), 2)
				the_loan.total_due_fees = total_loan_fees
				the_loan.total_due_penalty = 0.00
				the_loan.save()
				loan_schedules = LoanScheduler.objects.filter(loan = the_loan)
				get_interest = LoanScheduler.objects.filter(loan = the_loan)
				interest = []
				for i in get_interest:
					interest.append(i.interest)
				sum_interest=0
				for element in interest:
					sum_interest+=element
				total_due_interest = sum_interest + the_loan.principal_amount
				last_loan_schedules = LoanScheduler.objects.filter(loan = the_loan).last()
				next_loan_payment = LoanScheduler.objects.filter(loan=the_loan).filter(status='pending').first()
				Loan.objects.filter(id=the_loan.id).update(current_repayment_amount=next_loan_payment.due, interest=math.ceil(sum_interest), remaining_balance=math.ceil(principal_amount+float(sum_interest)), repayment_amount=math.ceil(principal_amount+float(sum_interest)), total_due_interest=math.ceil(sum_interest), maturity_date=last_loan_schedules.date)
				serializer = LoanSchedulerSerializer(loan_schedules, many=True)

				# return Response({"success": "loan has been disbursed", "schedules":serializer.data}, status=status.HTTP_201_CREATED)
				return Response({"success": res}, status=status.HTTP_201_CREATED)
			elif interest_method == 'Interest-Only':
				for duration in range(1, int(no_of_repayments) + 1):
					interest_only = Interest_Only(principal_amount, interest_rate, no_of_repayments)
					loan_repayment_amount = interest_only
					interestonly = interest_only

					my_fee = 0
					loan_fees = the_loan.loan_fees.all()
					for fees in loan_fees:
						my_fee += fees.amount

					loan_scheduler = LoanScheduler.objects.create(
						loan=the_loan,
						description = "Repayment",
						date=payment_date,
						principal = 0,
						interest = math.ceil(interestonly),
						fees = math.ceil(my_fee/the_loan.no_of_repayments),
						penalty = math.ceil(the_loan.penalty_amount/the_loan.no_of_repayments),
						due = math.ceil(interestonly),
						paid = 0.00,
						principal_paid = 0.00,
						pending_due = math.ceil(interestonly),
						total_due = math.ceil(interestonly),
						principal_due = 0,
						amount = math.ceil(the_loan.principal_amount),
						status = 'pending'
						)
					the_loan.interest_rate = Decimal(the_loan.interest_rate)
					the_loan.interest = interestonly
					the_loan.total_due_principal = principal_amount
					the_loan.total_due_interest = loan_repayment_amount
					the_loan.total_due_fees = the_loan.loan_fees
					the_loan.total_due_penalty = the_loan.penalty_amount
					the_loan.remaining_balance = loan_repayment_amount
					the_loan.repayment_amount = loan_repayment_amount
					the_loan.save()
					loan_schedules = LoanScheduler.objects.filter(loan = the_loan)
					last_loan_schedules = LoanScheduler.objects.filter(loan = the_loan).last()
					next_loan_payment = LoanScheduler.objects.filter(loan=the_loan).filter(status='pending').first()
					LoanScheduler.objects.filter(id = last_loan_schedules.id).update(amount=Decimal(last_loan_schedules.interest)+Decimal(the_loan.principal_amount))
					Loan.objects.filter(id=the_loan.id).update(maturity_date=last_loan_schedules.date, current_repayment_amount=next_loan_payment.due)
					serializer = LoanSchedulerSerializer(loan_schedules, many=True)
				# return Response({"message": "loan has been disbursed..." + " Total Interest to be paid is " + str(round(interestonly, 2)), "schedules":serializer.data}, status=status.HTTP_201_CREATED)
				return Response({"message": res}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	# def get(self, request, pk=None):
	#     loan = Loan.objects.all()
	#     serializer = LoanSerializer(loan, many=True)
	#     return Response(serializer.data)
	def get(self, request):
		ref = request.GET.get("ref")
		loan_status = request.GET.get("status")
		borrower = request.GET.get("borrower")
		guarantor = request.GET.get("guarantor")
		disbursed = request.GET.get("disbursed")
		approved = request.GET.get("approved")
		if ref: 
			try:
				loan = Loan.objects.get(pk=ref)
				serializer = LoanSerializer(loan)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except ObjectDoesNotExist:
				return Response({"message": "loan does not exist"},
								status=status.HTTP_404_NOT_FOUND)
		if loan_status:
			try:
				loan = Loan.objects.get(status=loan_status)
				serializer = LoanSerializer(loan)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except ObjectDoesNotExist:
				return Response({"message": "loan does not exist"},
								status=status.HTTP_404_NOT_FOUND)
		if disbursed and approved:
			queryset_list = Loan.objects.all()
			queryset_list = queryset_list.filter(disbursed=disbursed)
			queryset_list = queryset_list.filter(approved=approved)
			serializer = LoanSerializer(queryset_list, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		elif disbursed:
			try:
				loan = Loan.objects.filter(disbursed=disbursed)
				rez = []
				for each_loan_dis_app in loan:
					serializer = LoanSerializer(each_loan_dis_app).data
					rez.append(serializer)
				return Response(rez, status=status.HTTP_200_OK)
			except ObjectDoesNotExist:
				return Response({"message": "loan does not exist"},
								status=status.HTTP_404_NOT_FOUND)
		elif approved:
			try:
				loan = Loan.objects.filter(approved=approved)
				rez = []
				for each_loan_dis_app in loan:
					serializer = LoanSerializer(each_loan_dis_app).data
					rez.append(serializer)
				return Response(rez, status=status.HTTP_200_OK)
			except ObjectDoesNotExist:
				return Response({"message": "loan does not exist"},
								status=status.HTTP_404_NOT_FOUND)
		
		if borrower:
			loan = Loan.objects.filter(borrower=borrower)
			rez = []
			for each_loan in loan:             
				serializer = LoanSerializer(each_loan).data
				rez.append(serializer)
			return Response(rez, status=status.HTTP_200_OK)
		q = Loan.objects.all()
		serializer = LoanSerializer(q, many=True)
		return Response(serializer.data)

	# def get_object(self, pk):
	#     return Loan.objects.get(pk=pk)

	def patch(self, request, pk):
		# approved/decline loan by admin/staff
		# data = request.data
		# loan_id = data.get('id')
		try:
			loan = Loan.objects.get(pk=pk)
			loan.status = "restructured" 
			loan.save()    
			serializer = LoanSerializer(loan, data=request.data, partial = True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response({"message": "loan has been updated successful"})
		except ObjectDoesNotExist as error:
			return Response({"message": "loan with the id does not exist"},
							status=status.HTTP_404_NOT_FOUND)

	def delete(self, request, pk):
		loan = Loan.objects.get(pk=pk)
		loan.delete()
		return Response({"message": "loan deleted successfully!"})

class ApproveLoanRepaymentViewSet(ModelViewSet):
	serializer_class = LoanRepaymentSerializer
	queryset = LoanRepayment.objects.all()

	def partial_update(self, request, pk):
		loan_obj = self.get_object()
		get_loan_repayment = LoanRepayment.objects.get(id=loan_obj.id)
		if get_loan_repayment.status == 'rejected':
			return Response({"Error": "Repayment is declined and cannot be changed except delete."}, status=status.HTTP_400_BAD_REQUEST)
		if get_loan_repayment.status == 'accepted':
			return Response({"Error": "Repayment is approved and cannot be changed except delete."}, status=status.HTTP_400_BAD_REQUEST)
		serializer = LoanRepaymentSerializer2(loan_obj, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			obj = serializer.save()
			if obj.status == "accepted":
				collector = obj.collector
				collector = LoanOfficer.objects.get(pk = collector.id)
				amount = obj.amount
				sent_amount = amount
				loan = obj.loan.id
				repayment_mode = obj.repayment_mode
				comment = obj.comment
				date = obj.date
				payment_type = obj.payment_type
				proof_of_payment = obj.proof_of_payment
				the_loan = Loan.objects.get(pk = loan)
				loan_total_due_interest = the_loan.total_due_interest
				laon_interest = the_loan.interest
				# Loan.objects.filter(id=loan).update(amount_paid=new_amount)
				try:
					if(the_loan.amount_paid == None):
						the_loan.amount_paid = 0.00
					if(the_loan.remaining_balance == 0.00):
						the_loan.status = "fully paid"
					the_loan.amount_paid += amount
					the_loan.remaining_balance -= amount
					the_loan.total_due_interest -= amount
					the_loan.total_due_principal -= amount
					the_loan.save()
				except:
					pass
				get_schedule = LoanScheduler.objects.filter(loan = loan).order_by("date")
				get_last_schedule = LoanScheduler.objects.filter(loan = loan).last()
				get_last_schedule = LoanScheduler.objects.filter(loan = loan).filter(status='pending').first()
				# the_schedule = get_last_schedule
				get_pdue = LoanScheduler.objects.filter(loan = loan).order_by("date").exclude(status='settled').first()
				get_past_due = LoanScheduler.objects.filter(loan = loan).order_by("date").exclude(status='settled').first()
				get_next_due = LoanScheduler.objects.filter(loan = loan).order_by("date").exclude(status='settled').first()
				if get_past_due == None:
					past_due = datetime.date.today()
				else:
					past_due = get_past_due.date
				if get_next_due == None:
					next_due = datetime.date.today()
				else:
					next_due = get_next_due.date
				if get_pdue == None:
					pending_due = 0
				else:
					pending_due = get_pdue.pending_due
				if len(get_schedule) == 0:
					return Response({"msg":"open loan found"})

				for unit in get_schedule:
					if(unit.status != "settled"):
						if(Decimal(amount) <= unit.loan.repayment_amount) :
							unit.principal_due = Decimal(amount) - Decimal(unit.interest)
							unit.amount = unit.amount - unit.principal_due 
							unit.amount = unit.due
							unit.due = unit.total_due
							


							#unit.due -= Decimal(amount)
							#unit.paid += Decimal(amount)
							#unit.pending_due -= Decimal(amount)
							#unit.total_due -= Decimal(amount)
							#ppaid = Decimal(unit.paid) - Decimal(unit.interest)
							#if Decimal(amount) >= unit.interest:
							#	unit.principal_paid = ppaid
							#	unit.principal_due -= Decimal(unit.paid) - Decimal(unit.interest)
							#else:
							#	unit.principal_due -= Decimal(amount)
							#	unit.principal_paid = Decimal(unit.paid) - Decimal(unit.interest)
							# unit.principal_due -= int(amount)
							amount = 0
							unit.save()
						else:
							unit.status = "settled"
							unit.paid = unit.due
							unit.pending_due = 0
							unit.total_due = 0
							unit.principal_due = 0
							amount -= unit.due
							unit.amount = 0
							unit.save()
					else:
						pass
					# if(unit.status != "settled"):
					#     if(int(amount) <= int(unit.amount)):
					#         print("This")
					#         unit.amount -= int(amount)
					#         unit.paid += int(amount)
					#         unit.pending_due += int(amount)
					#         unit.total_due -= int(amount)
					#         ppaid = int(unit.paid) - int(unit.interest)
					#         if int(amount) >= unit.interest:
					#             unit.principal_paid = ppaid
					#             unit.principal_due -= int(unit.paid) - int(unit.interest)
					#         else:
					#             unit.principal_due -= int(amount)
					#             # unit.principal_paid = int(unit.paid) - int(unit.interest)
					#         amount = 0
					#         unit.save()
					#     elif(int(amount) > int(unit.amount)):
					#         print("That")
					#         # unit.amount -= int(amount)
					#         # unit.paid += int(amount)
					#         # unit.principal_paid += int(unit.paid) - int(unit.interest)
					#         unit.pending_due = 0
					#         unit.principal_due = 0
					#         unit.total_due = 0
					#         amount = 0
					#         unit.status = 'settled'
					#         unit.save()
					#     # elif(unit.status == "pending") and the_loan.amount_paid > 0 and the_loan.remaining_balance == 0:
					#     #     unit.status = "settled"
					#     #     print("Hmmmmm")
					#     #     unit.paid = unit.due
					#     #     unit.pending_due = 0
					#     #     unit.total_due = 0
					#     #     unit.principal_due = 0
					#     #     amount -= unit.amount
					#     #     unit.amount = 0
					#     #     unit.save()
					#     #     Loan.objects.filter(id=the_loan.id).update(status="fully paid")
					#     else:
					#         print("Finally")
					#         unit.status = "settled"
					#         # unit.principal_paid = int(unit.paid) - int(unit.interest)
					#         unit.paid = unit.due
					#         unit.pending_due = 0
					#         unit.total_due = 0
					#         unit.principal_due = 0
					#         amount -= unit.amount
					#         unit.amount = 0
					#         unit.save()

				loan_payment = LoanRepayment.objects.filter(id=obj.id).update(
					loan=the_loan,\
					date=datetime.date.today(),\
					amount=sent_amount,\
					repayment_mode = repayment_mode,\
					payment_type = payment_type,\
					proof_of_payment = proof_of_payment,\
					collector = collector,\
					comment = comment,\
					pending_due = pending_due,\
					past_due_date = past_due,\
					next_due_date = next_due,\
					status = 'accepted'
				)
				LoanScheduler.objects.filter(loan = the_loan)
				get_next_schedule = LoanScheduler.objects.filter(loan = loan).filter(status='pending').first()
				if get_next_schedule:
					Loan.objects.filter(id = the_loan.id).update(last_paid_date = datetime.date.today(), current_repayment_amount=get_next_schedule.due)
				serializer2 = LoanSchedulerSerializer(get_schedule, many=True)
				return Response({"msg": "repayment approved successfully","schedule": serializer2.data})



			elif obj.status == 'rejected':
				return Response({"message": "Repayment has been declined"}, status=status.HTTP_200_OK)
		return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoanCommentList(APIView):

	def post(self, request):
		# initialize a loan by customer
		serializer = LoanCommentSerializer(data=request.data)
		if serializer.is_valid():
			# save loan and send loan application email.
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, pk=None):
		loan_for = request.GET['loan']
		loan_comment = LoanComment.objects.filter(loan=int(loan_for))
		serializer = LoanCommentSerializer(loan_comment, many=True)
		return Response(serializer.data)


#class LoanFeeList(APIView):
 #   def post(self, request):
		# initialize a loan by customer
  #      serializer = LoanFeeSerializer(data=request.data)
   #     if serializer.is_valid():
			# save loan and send loan application email.
	  #      serializer.save()
	   #     return Response(serializer.data, status=status.HTTP_201_CREATED)
		#return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	#def get(self, request, pk=None):
	 #   loan_for = request.GET['loan']
	  #  loan_fee = LoanFee.objects.filter(loan=int(loan_for))
	   # serializer = LoanFeeSerializer(loan_fee, many=True)
		#return Response(serializer.data)
class LoanFeeViewSet(viewsets.ModelViewSet):
	serializer_class = LoanFeeSerializer
	queryset = LoanFee.objects.all()

class LoanToOfficer(APIView):
	def post(self, request):
		# initialize a loan by customer
		serializer = LoanMembershipSerializer(data=request.data)
		if serializer.is_valid():
			# save loan and send loan application email.
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, pk=None):
		#loan_for = request.GET['loan']
		loan_membership = LoanMembership.objects.filter(loan=pk)
		serializer = LoanMembershipSerializer(loan_membership, many=True)
		return Response(serializer.data)


class LoanCommentDetail(APIView):
	"""
	Retrieve, update or delete a snippet instance.
	"""

	def get_object(self, pk):
		try:
			return LoanComment.objects.get(pk=pk)
		except LoanComment.DoesNotExist:
			raise Http404

	def get(self, request, pk):
		loan_comment = self.get_object(pk)
		serializer = LoanCommentSerializer(loan_comment)
		return Response(serializer.data)

	def put(self, request, pk):
		loan_comment = self.get_object(pk)
		serializer = LoanCommentSerializer(loan_comment, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		loan_comment = self.get_object(pk)
		loan_comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class LoanOfficerList(APIView):
	
	def post(self, request):
		# initialize a loan by customer
		serializer = LoanOfficerSerializer(data=request.data)
		if serializer.is_valid():
			# save loan and send loan application email.
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, pk=None):
		loan_officer = LoanOfficer.objects.all()
		serializer = LoanOfficerSerializer(loan_officer, many=True)
		return Response(serializer.data)

class LoanOfficerDetail(APIView):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	def get_object(self, pk):
		try:
			return LoanOfficer.objects.get(pk=pk)
		except LoanOfficer.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		loan_officer = self.get_object(pk)
		serializer = LoanOfficerSerializer(loan_officer)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		loan_officer = self.get_object(pk)
		serializer = LoanOfficerSerializer(loan_officer, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		loan_officer = self.get_object(pk)
		loan_officer.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class PrincipalOutstandingLoan(APIView):
	def get(self, request, pk=None):
		principal_outstanding = Loan.objects.exclude(status="denied").exclude(status = "fully paid").exclude(status = "processing")
		output = []
		for unit in principal_outstanding:
			if unit.amount_paid < unit.principal_amount:
				principal_paid = unit.principal_amount - unit.amount_paid
			else:
				principal_paid = unit.principal_amount

			principal_due_till_today = 0
			filtered_loan_schedules = LoanScheduler.objects.filter(date__lte = datetime.date.today())
			for filtered_loan_schedule in filtered_loan_schedules:
				principal_due_till_today += principal_due

			

			rez = {'name': (unit.borrower.title + " "+ unit.borrower.first_name + " " + unit.borrower.last_name), 'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
					'principal': unit.principal_amount,
					'principal_paid': principal_paid,
					'principal_balance': str(int(unit.principal_amount) - int(unit.amount_paid)),
					'principal_due_till_today': principal_due_till_today,
					'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk),
					'principal_paid_till_today': principal_paid, 'principal_balance_till_today': (principal_due_till_today - principal_paid)}
			output.append(rez)
		# print(principal_outstanding)
		# serializer = LoanSerializer(principal_outstanding, many=True)
		return Response(output)


class TotalOpenLoans(APIView):
	def get(self, request, pk=None):
		open_loans = Loan.objects.exclude(status="denied").exclude(status = "fully paid").exclude(status="missed repayment")
		serializer = LoanSerializer(open_loans, many=True)
		return Response(serializer.data)


class InterestOutstandingLoan(APIView):
	def get(self, request, pk=None):
		principal_outstanding = Loan.objects.filter(status="current")
		output = []
		for unit in principal_outstanding:
			if unit.repayment_amount is None:
				unit.repayment_amount = 0.00
			if unit.amount_paid is None:
				unit.amount_paid = 0
			interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
			if int(unit.amount_paid) > int(unit.principal_amount):
				interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
			if unit.repayment_amount < unit.principal_amount:
				rez = {'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
					   'principal': unit.principal_amount,
					   'principal_paid': unit.amount_paid, 'interest_oustanding': str(interest_amount),
					   'principal_due_till_today': unit.remaining_balance,
					   'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk)}
				output.append(rez)
			else:
				pass
		# print(principal_outstanding)
		# serializer = LoanSerializer(principal_outstanding, many=True)
		return Response(output)


#getting the loan by category
class SearchLoanType(APIView):
	def get(self, request, pk=None):
		loan_type = request.GET.get("loan_type")
		#loans = LoanType.objects.filter(status = loan_type.name)[0]
		category = LoanType.objects.get(name=loan_type)
		loans = Loan.objects.filter(loan_type = category)
		serializer = LoanSerializer(loans[0])
		return Response(serializer.data)


		
class FullyPaidLoans(APIView):
	def get(self, request, pk=None):
		fully_paid = Loan.objects.filter(status="fully paid")
		serializer = LoanSerializer(fully_paid, many=True)
		return Response(serializer.data)


class LoansByOfficers(APIView):
	def get(self, request, pk=None):  
		loan_officer = LoanOfficer.objects.filter(pk = pk)
		total = []
		serializer = LoanSerializer(rez, many=True)         
		return Response(serializer.data)


class FeesOutstandingLoan(APIView):
	def get(self, request, pk=None):
		fees_outstanding = Loan.objects.filter(loan_fees__gt = 0)
		# output = []
		# for unit in fees_outstanding:
		#     if unit.repayment_amount is None:
		#         unit.repayment_amount = 0.00
		#     if unit.amount_paid is None:
		#         unit.amount_paid = 0
		#     interest_amount = int(unit.repayment_amount) - int(unit.principal_amount)
		#     if int(unit.amount_paid) > int(unit.principal_amount):
		#         interest_amount = interest_amount - int(unit.amount_paid) - int(unit.principal_amount)
		#     if unit.repayment_amount < unit.principal_amount:
		#         rez = {'loan_id': unit.pk, 'released': unit.loan_release_date, 'maturity': unit.maturity_date,
		#                'principal': unit.principal_amount,
		#                'principal_paid': unit.amount_paid, 'remaining_balance': unit.remaining_balance,
		#                'principal_due_till_today': unit.remaining_balance,
		#                'status': unit.status, 'branch': str(unit.branch.pk), 'borrower': str(unit.borrower.pk)}
		#         output.append(rez)

			# else:
			#     pass
		# print(principal_outstanding)
		serializer = LoanSerializer(fees_outstanding, many=True).data
		return Response(serializer)


class LoanRepaymentViewSet(ModelViewSet):
    serializer_class = LoanRepaymentSerializer

    def get_queryset(self):
        req = self.request
        borrower = req.query_params.get('borrower')
        branch = req.query_params.get('branch')
        if borrower:
            self.queryset = LoanRepayment.objects.filter(loan__borrower__pk=borrower)
            return self.queryset
        if branch:
            self.queryset = LoanRepayment.objects.filter(loan__branch__pk=branch)
            return self.queryset
        else:
            self.queryset = LoanRepayment.objects.all()
            return self.queryset

    def create(self, request, *args, **kwargs):
        see_loan = Loan.objects.filter(id=request.data['loan'])
        the_amount = request.data['amount']
        if see_loan:
            get_d_loan = Loan.objects.get(id=request.data['loan'])
            if float(the_amount) > float(get_d_loan.remaining_balance):
                return Response({'Error': "Sorry you cannot pay more than "+str(get_d_loan.remaining_balance)}, status=status.HTTP_400_BAD_REQUEST)
            if get_d_loan.remaining_balance == 0.00:
                return Response({"Error": "Sorry, this loan has been settled"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = LoanRepaymentSerializer2(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    obj = serializer.save()
                    if obj:
                        collector = obj.collector
                        collector = LoanOfficer.objects.get(pk = collector.id)
                        amount = obj.amount
                        sent_amount = amount
                        loan = obj.loan.id
                        repayment_mode = obj.repayment_mode
                        comment = obj.comment
                        date = obj.date
                        payment_type = obj.payment_type
                        proof_of_payment = obj.proof_of_payment
                        the_loan = Loan.objects.get(pk = loan)
                    return Response({"Repayment awaiting approval": serializer.data}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Loan Does not Exists"}, status=status.HTTP_400_BAD_REQUEST)



class LoanTypeViewSet(ModelViewSet):
	serializer_class = LoanTypeSerializer

	def get_queryset(self):
		queryset = LoanType.objects.all()
		return queryset

class LoanCollateralViewSet(ModelViewSet):
	serializer_class = LoanCollateralSerializer

	def get_queryset(self):
		queryset = LoanCollateral.objects.all()
		borrower = self.request.GET.get('borrower')
		branch = self.request.GET.get('branch')
		if branch:
			queryset.filter(loan__branch__pk=branch)
		if borrower:
			queryset.filter(loan__borrower__pk=borrower)

		return queryset


class LoanGuarantorViewSet(ModelViewSet):
	serializer_class = LoanGuarantorSerializer

	def get_queryset(self):
		queryset = LoanGuarantor.objects.all()
		borrower = self.request.GET.get('borrower')
		branch = self.request.GET.get('branch')
		if branch:
			queryset.filter(loan__branch__pk=branch)
		if borrower:
			queryset.filter(loan__borrower__pk=borrower)

		return queryset


	def create(self, request, *args, **kwargs):
		check_branch = Branch.objects.filter(id=request.data['branch']).exists()
		if check_branch:
			get_branch = Branch.objects.get(id=request.data['branch'])
		if get_branch.is_open == False:
			return Response({"Error": "Selected Branch is not opened yet. Choose another branch for this guarantor."}, status=status.HTTP_400_BAD_REQUEST)
		if request.data['photo'] != '':
			upload_data = cloudinary.uploader.upload(request.data['photo'], resource_type="auto")
			request.data['photo'] = upload_data['secure_url']
		serializer = LoanGuarantorSerializer2(data=request.data)
		serializer.is_valid(raise_exception=True)
		# instance = self.perform_create(serializer)

		serializer.save()
		obj = serializer.save()

		return Response(serializer.data)

	def partial_update(self, request, pk=None):
		instance = self.get_object()
		if request.data['photo'] != '':
			upload_data = cloudinary.uploader.upload(request.data['photo'], resource_type="auto")
			request.data['photo'] = upload_data['secure_url']
		serializer = LoanGuarantorSerializer2(instance, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoanDisbursementViewSet(ModelViewSet):
	serializer_class = LoanDisbursementSerializer

	def get_queryset(self):
		queryset = LoanDisbursement.objects.all()
		borrower = self.request.GET.get('borrower')
		branch = self.request.GET.get('branch')
		if branch:
			queryset.filter(loan__branch__pk=branch)
		if borrower:
			queryset.filter(loan__borrower__pk=borrower)

		return queryset

	def create(self, request, *args, **kwargs):
		# chk_loan = Loan.objects.filter(id=request.data['loan']).exists()
		# if chk_loan:
		#     get_loan = Loan.objects.get(id=request.data['loan'])
		#     if get_loan.approved == False:
		#         return Response({"message": "Sorry, this loan is waiting approval"}, status=status.HTTP_400_BAD_REQUEST)
		#     else:
		flt_loan_status = Loan.objects.filter(id=request.data['loan'])
		d_loan_obj = Loan.objects.get(id=request.data['loan'])
		if flt_loan_status:
			get_the_loan = Loan.objects.get(id=request.data['loan'])
			branch_remaining_capital = d_loan_obj.branch.remaining_capital
			branch_spent_capital = d_loan_obj.branch.spent_capital
			branch_min_loan_amount = d_loan_obj.branch.min_loan_amount
			branch_max_loan_amount = d_loan_obj.branch.max_loan_amount
			branch_min_loan_interest = d_loan_obj.branch.min_loan_interest
			branch_max_loan_interest = d_loan_obj.branch.max_loan_interest

			# if Decimal(request.data['disbursed_amount']) > Decimal(branch_remaining_capital):
			#     return Response({"Error": "Sorry, Branch Capital Balance is less than the disbursing amount."}, status=status.HTTP_400_BAD_REQUEST)
			if Decimal(request.data['disbursed_amount']) > Decimal(branch_max_loan_amount):
				return Response({"Error": "Sorry, disbursing amount is higher than the Branch Maximum Loan Amount."}, status=status.HTTP_400_BAD_REQUEST)
			# if Decimal(request.data['disbursed_amount']) < Decimal(branch_min_loan_amount):
			#     return Response({"Error": "Sorry, Approving amount is lower than the Branch Maximum Loan Amount."}, status=status.HTTP_400_BAD_REQUEST)
			# if loan_obj.interest_mode == 'Percentage Based' and loan_obj.loan_type.interest_rate < Decimal(branch_min_loan_interest):
			#     return Response({"Error": "Sorry, Interest rate is lower than the Branch Minimum Loan Interest."}, status=status.HTTP_400_BAD_REQUEST)
			# if loan_obj.interest_mode == 'Percentage Based' and loan_obj.loan_type.interest_rate > Decimal(branch_max_loan_interest):
			#     return Response({"Error": "Sorry, Interest rate is higher than the Branch Maximum Loan Interest."}, status=status.HTTP_400_BAD_REQUEST)

			if get_the_loan.status == 'denied':
				return Response({"Error": "This loan has been declined and cannot accept disbursement"}, status=status.HTTP_400_BAD_REQUEST)
			elif get_the_loan.approved == False:
				return Response({"Error": "This Loan has not been approved yet."}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"Error": "Loan Does not exist"}, status=status.HTTP_404_NOT_FOUND)

		serializer = LoanDisbursementSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		# Loan.objects.filter(id=request.data['loan']).update(principal_amount=request.data['disbursed_amount'], amount_to_borrower=request.data['disbursed_amount'])
		serializer.save()
		obj = request.data
		flt_loan = Loan.objects.get(id=obj["loan"])
		if flt_loan.disbursed == True:
			return Response({"Error": "Loan already disbursed"}, status=status.HTTP_400_BAD_REQUEST)
		the_loan = Loan.objects.get(id=obj["loan"])
		loan_obj = Loan.objects.get(id=obj["loan"])
		# print(loan_obj.loan_type.interest_rate)
		loan_status = the_loan.status
		if loan_status and (loan_status == 'approved' or loan_status == 'restructured'):
			new_loan = Loan.objects.get(id=the_loan.id)
			new_loan.amount_to_borrower = Decimal(request.data['disbursed_amount'])
			new_loan.disbursed = True
			new_loan.staff_permission_disbursed = True
			new_loan.status = "current"
			new_loan.branch.spent_capital += int(obj["disbursed_amount"])
			remaining_capital = Decimal(loan_obj.branch.capital) - Decimal(loan_obj.branch.spent_capital)
			Branch.objects.filter(id=new_loan.branch.id).update(remaining_capital=remaining_capital)
			new_loan.save()
			return Response({'success': 'Loan has been disbursed successfully'}, status=status.HTTP_200_OK)
		serializer.save()
		obj = serializer.save()
		return Response(serializer.data) 


class GuarantorFileViewSet(ModelViewSet):
	serializer_class = GuarantorFileSerializer

	def get_queryset(self):
		queryset = GuarantorFile.objects.all()

		return queryset


class RunBvnCheck(APIView):

	def post(self, request):
		profile = request.data.get("profile")
		bvn = request.data.get("bvn")
		dob = request.data.get("dob")
		reference_no = 'loanx' + str(random.randint(100000000, 999999999))
		rez = details_from_bvn(bvn, reference_no)
		if rez == False:
			return Response({"message": "Error BVN Details"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			# print(rez['date_of_birth'])
			dob_check = (compare_dates(rez['date_of_birth'], dob))
			print(dob_check)
			if not dob_check:
				return Response({"message": "non-matching credentials provided"},
								status=status.HTTP_400_BAD_REQUEST)
		try:
			profile_obj = User.objects.get(pk=profile)
			try:
				profile_obj.gender = rez['gender']
			except:
				pass
			try:
				profile_obj.last_name = rez['last_name']
			except:
				pass
			try:
				profile_obj.first_name = rez['first_name']
			except:
				pass
			try:
				profile_obj.middle_name = rez['middle_name']
			except:
				pass
			try:
				profile_obj.email = rez['email']
			except:
				pass
			try:
				profile_obj.address = rez['residential_address']
			except:
				pass
			try:
				profile_obj.city = rez['city']
			except:
				pass
			try:
				profile_obj.date_of_birth = dob
			except:
				pass
			try:
				profile_obj.bvn = bvn
			except:
				pass
			try:
				profile_obj.email = rez['email']
			except:
				pass
			try:
				profile_obj.phone = rez['phone_number']
			except:
				pass
			profile_obj.save()
			return Response({"message": rez}, status=status.HTTP_200_OK)
		except User.DoesNotExist as err:
			return Response({"message": "User with the id does not exist"},
							status=status.HTTP_404_NOT_FOUND)


class GetAccountName(APIView):

	def post(self, request):
		account_number = request.data.get("account_number")
		bank_code = request.data.get("bank_code")
		ref = 'loanx' + str(random.randint(100000000, 999999999))
		rez = get_account_name(account_number, bank_code, ref)
		if rez == False:
			return Response({"message": "Either Account Number/Selected Bank does not match."}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"message": rez},status=status.HTTP_200_OK)


class GetLoanScore(APIView):
	def post(self, request):
		amount = request.data.get("amount")
		borrower = request.data.get('borrower')
		phone = request.data.get('phone')
		reference_no = 'loanx' + str(random.randint(100000000, 999999999))
		borrower = Borrower.objects.get(pk=borrower)
		rez = get_loan_score(phone, reference_no, borrower.first_name, borrower.last_name, borrower.email, amount)
		print(rez)
		try:
			try:
				if rez['score']:
					borrower.loan_score = rez['score']
					borrower.save()
			except:
				pass
			serializer = BorrowerSerializer(borrower).data
			#borrower_groups = Loan.objects.filter(borrower=borrower).update()
			# return Response({"message": rez}, status=status.HTTP_200_OK)
			return Response(serializer, status=status.HTTP_200_OK)
		except Borrower.DoesNotExist:
			return Response({'message': 'borrower with the borrower id does not exist'},
							status=status.HTTP_404_NOT_FOUND)
#     def get_queryset(self):
#         queryset = LoanRepayment.objects.all()
#         borrower = self.request.GET.get('borrower')
#         if borrower:
#             queryset.filter(loan_schedule__loan__borrower__pk=borrower)

#         return queryset

class LoanCollateralList(APIView):
	parser_class = (FileUploadParser,)
	def post(self, request):
		# initialize a loan by customer
		serializer = LoanCollateralSerializer(data=request.data)
		if serializer.is_valid():
			# save loan and send loan application email.
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, pk=None):
		loan_collateral = LoanCollateral.objects.all()
		serializer = LoanCollateralSerializer(loan_collateral, many=True)
		return Response(serializer.data)

class LoanCollateralDetail(APIView):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	def get_object(self, pk):
		try:
			return LoanCollateral.objects.get(pk=pk)
		except LoanCollateral.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		loan_collateral = self.get_object(pk)
		serializer = LoanCollateralSerializer(loan_collateral)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		loan_collateral = self.get_object(pk)
		serializer = LoanCollateralSerializer(loan_collateral, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		loan_collateral = self.get_object(pk)
		loan_collateral.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



class LoanAttachmentList(APIView):
	parser_class = (FileUploadParser,)
	def post(self, request):
		# initialize a loan by customer
		serializer = LoanAttachmentSerializer(data=request.data)
		if serializer.is_valid():
			# save loan and send loan application email.
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, pk=None):
		loan_attachment = LoanAttachment.objects.filter(loan = loan)
		serializer = LoanAttachmentSerializer(loan_attachment, many=True)
		return Response(serializer.data)

class LoanAttachmentDetail(APIView):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	def get_object(self, pk):
		try:
			return LoanAttachment.objects.get(pk=pk)
		except LoanAttachment.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		loan_attachment = self.get_object(pk)
		serializer = LoanAttachmentSerializer(loan_attachment)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		loan_attachment = self.get_object(pk)
		serializer = LoanAttachmentSerializer(loan_attachment, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		loan_attachment = self.get_object(pk)
		loan_attachment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class ApproveOrDeclineLoan(APIView):

	def post(self, request):
		loan = int(request.data.get('loan'))
		amount = request.data.get('amount')
		staff_id = request.data.get('staff')
		check_staff = Staff.objects.filter(id=staff_id).exists()
		new_loan_obj = Loan.objects.get(pk=loan)
		if check_staff == False:
			return Response({'error': 'Sorry, no staff with such ID'}, status=status.HTTP_404_NOT_FOUND)
		staff = Staff.objects.get(id=staff_id)
		if new_loan_obj.approval_level > 3:
			return Response({'error': 'This loan has already been approved by the third level approval'})
		check_approved = LoanApproval.objects.filter(staff=staff, loan=new_loan_obj).exists()
		if check_approved == True:
			get_approved = LoanApproval.objects.filter(staff=staff, loan=new_loan_obj).last()
			return Response({'error': 'Sorry, this staff has already '+get_approved.decision+' this loan.'}, status=status.HTTP_400_BAD_REQUEST)
		if amount:
			amount = float(amount)
			principal_amount = float(amount)
		duration = request.data.get('duration')
		if duration:
			duration = int(duration)
		loan_duration_period = request.data.get('loan_duration_period')
		repayment_cycles = request.data.get('repayment_cycles')
		no_of_repayments = request.data.get('no_of_repayments')
		if no_of_repayments:
			no_of_repayments = int(no_of_repayments)
		loan_interest_percentage_period = request.data.get('loan_interest_percentage_period')
		loan_interest_percentage = request.data.get('loan_interest_percentage')
		if loan_interest_percentage:
			loan_interest_percentage = float(loan_interest_percentage)
		decision = request.data.get('decision', None)
		if decision == "approve":
			loan_obj = Loan.objects.filter(pk=loan).first()
			branch_capital = loan_obj.branch.capital
			branch_remaining_capital = loan_obj.branch.remaining_capital
			branch_spent_capital = loan_obj.branch.spent_capital
			branch_min_loan_amount = loan_obj.branch.min_loan_amount
			branch_max_loan_amount = loan_obj.branch.max_loan_amount
			branch_min_loan_interest = loan_obj.branch.min_loan_interest
			branch_max_loan_interest = loan_obj.branch.max_loan_interest

			### Loan
			interest_mode = loan_obj.interest_mode
			loan_interest_percentage = loan_obj.loan_interest_percentage
			loan_interest_fixed_amount = loan_obj.loan_interest_fixed_amount
			loan_interest_percentage_period = loan_obj.loan_interest_percentage_period
			# loan_interest = (loan_obj.loan_interest_percentage)/100
			####

			if Decimal(amount) > Decimal(branch_remaining_capital):
				return Response({"Error": "Sorry, Branch Capital Balance is less than the approving amount."}, status=status.HTTP_400_BAD_REQUEST)
			if Decimal(amount) > Decimal(branch_max_loan_amount):
				return Response({"Error": "Sorry, Approving amount is higher than the Branch Maximum Loan Amount."}, status=status.HTTP_400_BAD_REQUEST)
			if Decimal(amount) < Decimal(branch_min_loan_amount):
				return Response({"Error": "Sorry, Approving amount is lower than the Branch Maximum Loan Amount."}, status=status.HTTP_400_BAD_REQUEST)
			if loan_obj.interest_mode == 'Percentage Based' and loan_obj.loan_type.interest_rate < Decimal(branch_min_loan_interest):
				return Response({"Error": "Sorry, Interest rate is lower than the Branch Minimum Loan Interest."}, status=status.HTTP_400_BAD_REQUEST)
			if loan_obj.interest_mode == 'Percentage Based' and loan_obj.loan_type.interest_rate > Decimal(branch_max_loan_interest):
				return Response({"Error": "Sorry, Interest rate is higher than the Branch Maximum Loan Interest."}, status=status.HTTP_400_BAD_REQUEST)
			loan_status = loan_obj.status
			total_loan_fees = 0.0
			loan_fixed_amount = 0.00
			LoanApproval.objects.create(decision='approved', staff=staff, loan=loan_obj)
			fetch_approval = LoanApproval.objects.filter(loan=new_loan_obj)
			total_approval_count = len(fetch_approval)
			if loan_obj.loan_interest_fixed_amount != 'null':
				loan_fixed_amount = loan_obj.loan_interest_fixed_amount
			total_repayment_amount = int(amount)
			for loan_fee in loan_obj.loan_fees.all():
				if loan_fee.interest_type == 'Percentage Based':
					total_due_interest = float((loan_obj.interest/100)*Decimal(amount))
					total_loan_fees = int(total_loan_fees)
					amount_to_borrower = total_repayment_amount - int((loan_fee.percentage/100)*Decimal(amount))
					amount_to_borrower = int(total_repayment_amount)
				elif loan_fee.interest_type == 'Fixed Amount Per Cycle':
					# total_loan_fees += float(loan_fee.amount)
					total_loan_fees += float(loan_fixed_amount)
					total_loan_fees = int(total_loan_fees)
					# total_repayment_amount -= int(loan_fee.amount)
					amount_to_borrower -= int(loan_fixed_amount)
					amount_to_borrower = int(total_repayment_amount)
			# loan_obj.loan_fees.amount = total_loan_fees
			# print(total_repayment_amount)
			# print(total_loan_fees)
			if loan_obj.status == 'denied':
				return Response({'error': 'Sorry, loan was declined. Try a new loan.'}, status=status.HTTP_400_BAD_REQUEST)
			if loan_obj.approved==True and loan_obj.disbursed==False:
				return Response({"message": "This loan has already been approved but waiting for disbursement"}, status=status.HTTP_400_BAD_REQUEST)
			elif loan_obj.approved==True and loan_obj.disbursed==True:
				return Response({"message": "This loan has already been approved and has also been disbursed"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				# Return Back the loan ID that was created...
				the_loan = Loan.objects.get(id=loan)
				# loan_interest_percentage = float(the_loan.loan_interest_percentage)
				# principal_amount = float(amount)
				# no_of_repayments = int(the_loan.no_of_repayments)
				interest_method = the_loan.interest_method
				# loan_duration_period = the_loan.loan_duration_period
				# repayment_cycles = the_loan.repayment_cycles
				# duration = int(the_loan.duration)
				# interest_rate = float(the_loan.loan_interest_percentage)
				# loan_interest_percentage_period = the_loan.loan_interest_percentage_period

				interest = float(loan_interest_percentage)/100
				loan_interest = float(principal_amount)*interest
				principal_payment = round(float(principal_amount)/float(no_of_repayments), 2)
				current_time = today
				payment_date = current_time
				amount = principal_amount
				try:
					existing_schedules = LoanScheduler.objects.filter(loan = the_loan).delete()
				except:
					pass

				if interest_method == 'Flat Rate':
					repayment_amount = round((loan_interest)+(principal_payment), 2)
					flat_rate = Flat_Rate(float(principal_amount), float(loan_interest_percentage), int(no_of_repayments))
					loan_repayment_amount = flat_rate+principal_amount
					principal_due = principal_amount/no_of_repayments

					for duration in range(1, int(no_of_repayments) + 1):
						payment_dates = get_payment_dates(loan_duration_period, repayment_cycles, current_time, duration, payment_date)

						off_principal = round((principal_amount)/(no_of_repayments), 2)
						off_interest = round((flat_rate)/(no_of_repayments), 2)
						total_due = round(float(off_principal)+float(off_interest), 2)
						off_paid = 0.00
						d_due = round((principal_amount)/(no_of_repayments), 2)
						d_due2 = round((flat_rate)/(no_of_repayments), 2)
						d_due3 = round((d_due)+(d_due2), 2)
						new_payment = float(off_principal)+float(off_interest)
						pending_due = float(total_due)-float(the_loan.amount_paid)
						principal_payment -= float(principal_amount/no_of_repayments)
						principal_payment = round((principal_payment) + float(principal_amount/no_of_repayments), 2)
						total_due_amount = round(d_due3 * no_of_repayments, 2)

						principal_schedule = principal_amount/no_of_repayments
						increasing_principal = principal_schedule - principal_due
						principal_amt = principal_amount/no_of_repayments
						amount -= principal_amt
						increasing_principal = round((amount) + float(principal_schedule), 2)


						my_fee = 0

						loan_fees = the_loan.loan_fees.all()
						for fees in loan_fees:
							my_fee += fees.amount

						loan_scheduler = LoanScheduler.objects.create(
							loan=the_loan,
							description = "Repayment",
							date=payment_dates,
							principal = off_principal,
							interest = off_interest,
							fees = round(my_fee/the_loan.no_of_repayments, 2),
							penalty = round(the_loan.penalty_amount/the_loan.no_of_repayments, 2),
							due = d_due3,
							paid = 0.00,
							principal_paid = 0.00,
							pending_due = round(pending_due, 2),
							total_due = round(total_due, 2),
							principal_due = off_principal,
							amount=increasing_principal,
							status='pending'
						)

					the_loan.loan_interest_percentage = Decimal(loan_interest_percentage)
					loan_interest += (float(loan_interest_percentage)/100) * principal_amount
					the_loan.interest = Decimal(flat_rate)
					the_loan.principal_amount = principal_amount
					the_loan.total_due_principal = principal_amount
					the_loan.total_due_interest = loan_repayment_amount
					the_loan.total_due_fees = the_loan.loan_fees
					the_loan.total_due_penalty = the_loan.penalty_amount
					the_loan.loan_release_date = current_time
					the_loan.remaining_balance = loan_repayment_amount
					the_loan.repayment_amount = loan_repayment_amount
					if total_approval_count == 1:
						the_loan.approved = True
						the_loan.approval_level = 3
						the_loan.third_approval = staff
						the_loan.status = "approved"
						the_loan.staff_permission_approved = True
						the_loan.staff_permission_accepted = True
					elif total_approval_count == 2:
						the_loan.approval_level = 2
						the_loan.second_approval = staff
						the_loan.staff_permission_approved = True
					elif total_approval_count == 3:
						the_loan.approved = True
						the_loan.approval_level = 3
						the_loan.third_approval = staff
						the_loan.status = "approved"
					the_loan.save()
					loan_schedules = LoanScheduler.objects.filter(loan = the_loan)
					last_loan_schedules = LoanScheduler.objects.filter(loan = the_loan).last()
					next_loan_payment = LoanScheduler.objects.filter(loan=the_loan).filter(status='pending').first()
					Loan.objects.filter(id=the_loan.id).update(maturity_date=last_loan_schedules.date, current_repayment_amount=next_loan_payment.due)
					serializer = LoanSchedulerSerializer(loan_schedules, many=True)

					return Response({"message": "Loan has been approved", "schedules": serializer.data}, status=status.HTTP_201_CREATED)

				elif interest_method == 'Reducing Balance - Equal Principal':
					if loan_duration_period == "Days":
						period = int_day(duration, loan_interest_percentage_period, loan_duration_period, interest)
						equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)
					elif loan_duration_period == "Weeks":
						period = int_week(duration, loan_interest_percentage_period, loan_duration_period, interest)
						equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)
					elif loan_duration_period == "Months":
						period = int_month(duration, loan_interest_percentage_period, loan_duration_period, interest)
						equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)
					elif loan_duration_period == "Years":
						period = int_year(duration, loan_interest_percentage_period, loan_duration_period, interest)
						equal_principal = Equal_Principal(principal_amount, duration, loan_interest_percentage_period, loan_duration_period, interest, principal_payment, period)

					equal_principal = round(equal_principal, 2)
					interest_schedule = equal_principal/no_of_repayments
					principal_due = principal_amount/no_of_repayments

					pend_due = float(principal_amount)/float(no_of_repayments)
					pend_due = pend_due+float(equal_principal)
					principal_plus_interest = 0.0
					total_interest = 0
					loan_amount = principal_amount
					total_loan_fees = 0.0
					total_repayment_amount_per_schedule = principal_amount / no_of_repayments

					for duration in range(1, int(no_of_repayments) + 1):
						payment_dates = get_payment_dates(loan_duration_period, repayment_cycles, current_time, duration, payment_date)
						repayment_schedule = principal_due + (float(principal_amount) * (float(loan_interest_percentage) / 100))
						principal_plus_interest += repayment_schedule

						due = float(principal_amount)/float(no_of_repayments)
						due = due+float(equal_principal)

						equal_principal -= round(interest_schedule, 2)
						reducing_interest = equal_principal+interest_schedule

						principal_schedule = principal_amount/no_of_repayments
						increasing_principal = principal_schedule - principal_due
						principal_amt = principal_amount/no_of_repayments
						loan_amount -= principal_amt
						increasing_principal = round((loan_amount) + float(principal_schedule), 2)


						pen_due = (float(principal_amount)/float(no_of_repayments)) + float(equal_principal)
						pend_due += float(due) - float(interest_schedule)
						pending_due = (pend_due - pen_due)
						total_due = (pend_due - pen_due)

						loan_scheduler = LoanScheduler.objects.create(
							loan=the_loan,
							description = "Repayment",
							date=payment_dates,
							principal = round(Decimal(principal_amount)/Decimal(no_of_repayments), 2),
							interest = round(reducing_interest, 2),
							fees = total_loan_fees/no_of_repayments,
							penalty = 0.00,
							due=round(due, 2),
							paid = 0.00,
							pending_due = round(pending_due, 2),
							total_due = total_due,
							principal_due = round(increasing_principal, 2),
							amount = round(increasing_principal, 2),
							# Principal Outstanding - Principal Due [for each cycle] (Reducing),
							status='pending'
							)
						# principal_amount -= total_repayment_amount_per_schedule
						loan_fees = the_loan.loan_fees.all()
						total_loan_fee = 0.0
						the_loan.interest = equal_principal
					the_loan.total_due_principal = round((principal_amount)/(no_of_repayments) * (no_of_repayments), 2)
					the_loan.total_due_fees = total_loan_fees
					the_loan.total_due_penalty = 0.00
					the_loan.principal_amount = principal_amount
					if total_approval_count == 1:
						the_loan.staff_permission_accepted = True
						the_loan.approval_level = 1
						the_loan.first_approval = staff
					elif total_approval_count == 2:
						the_loan.staff_permission_approved = True
						the_loan.approval_level = 2
						the_loan.second_approval = staff
					elif total_approval_count == 3:
						the_loan.approved = True
						the_loan.approval_level = 3
						the_loan.third_approval = staff
						the_loan.status = "approved"
					the_loan.save()
					loan_schedules = LoanScheduler.objects.filter(loan = the_loan)
					get_interest = LoanScheduler.objects.filter(loan = the_loan)
					interest = []
					for i in get_interest:
						interest.append(i.interest)
					sum_interest=0
					for element in interest:
						sum_interest+=float(element)
					total_due_interest = sum_interest + principal_amount
					last_loan_schedules = LoanScheduler.objects.filter(loan = the_loan).last()
					next_loan_payment = LoanScheduler.objects.filter(loan=the_loan).filter(status='pending').first()
					Loan.objects.filter(id=the_loan.id).update(current_repayment_amount=next_loan_payment.due, interest=math.ceil(sum_interest), remaining_balance=math.ceil(principal_amount+float(sum_interest)), repayment_amount=math.ceil(principal_amount+float(sum_interest)), total_due_interest=math.ceil(sum_interest), maturity_date=last_loan_schedules.date)
					serializer = LoanSchedulerSerializer(loan_schedules, many=True)

					# return Response({"success": "loan has been disbursed", "schedules":serializer.data}, status=status.HTTP_201_CREATED)
					return Response({"success": "Loan has been approved", "schedules": serializer.data}, status=status.HTTP_201_CREATED)
				elif interest_method == 'Interest-Only':
					for duration in range(1, int(no_of_repayments) + 1):
						interest_only = Interest_Only(float(principal_amount), float(loan_interest_percentage), int(no_of_repayments))
						loan_repayment_amount = interest_only
						interestonly = interest_only

						my_fee = 0
						loan_fees = the_loan.loan_fees.all()
						for fees in loan_fees:
							my_fee += fees.amount

						loan_scheduler = LoanScheduler.objects.create(
							loan=the_loan,
							description = "Repayment",
							date=payment_date,
							principal = 0,
							interest = math.ceil(interestonly),
							fees = math.ceil(my_fee/the_loan.no_of_repayments),
							penalty = math.ceil(the_loan.penalty_amount/the_loan.no_of_repayments),
							due = math.ceil(interestonly),
							paid = 0.00,
							principal_paid = 0.00,
							pending_due = math.ceil(interestonly),
							total_due = math.ceil(interestonly),
							principal_due = 0,
							amount = math.ceil(the_loan.principal_amount),
							status = 'pending'
							)
						the_loan.interest_rate = Decimal(the_loan.interest_rate)
						the_loan.interest = interestonly
						the_loan.total_due_principal = principal_amount
						the_loan.total_due_interest = loan_repayment_amount
						the_loan.total_due_fees = the_loan.loan_fees
						the_loan.total_due_penalty = the_loan.penalty_amount
						the_loan.remaining_balance = loan_repayment_amount
						the_loan.repayment_amount = loan_repayment_amount
						the_loan.principal_amount = principal_amount
						if total_approval_count == 1:
							the_loan.first_approval = staff
							the_loan.approval_level = 1
							the_loan.staff_permission_accepted = True
						elif total_approval_count == 2:
							the_loan.second_approval = staff
							the_loan.approval_level = 2
							the_loan.staff_permission_approved = True
						elif total_approval_count == 3:
							the_loan.approved = True
							the_loan.approval_level = 3
							the_loan.third_approval = staff
							the_loan.status = "approved"
						the_loan.save()
						loan_schedules = LoanScheduler.objects.filter(loan = the_loan)
						last_loan_schedules = LoanScheduler.objects.filter(loan = the_loan).last()
						next_loan_payment = LoanScheduler.objects.filter(loan=the_loan).filter(status='pending').first()
						LoanScheduler.objects.filter(id = last_loan_schedules.id).update(amount=Decimal(last_loan_schedules.interest)+Decimal(the_loan.principal_amount))
						Loan.objects.filter(id=the_loan.id).update(maturity_date=last_loan_schedules.date, current_repayment_amount=next_loan_payment.due)
						serializer = LoanSchedulerSerializer(loan_schedules, many=True)
					# return Response({"message": "loan has been disbursed..." + " Total Interest to be paid is " + str(round(interestonly, 2)), "schedules":serializer.data}, status=status.HTTP_201_CREATED)
					return Response({"message": "Loan has been approved", "schedules": serializer.data}, status=status.HTTP_201_CREATED)
				# Loan.objects.filter(id=loan_obj.id).update(amount_to_borrower=amount_to_borrower, principal_amount=amount, approved=True, status='approved', staff_permission_accepted=True)
				# return Response({"message": "Loan Approved Successfully"}, status=status.HTTP_200_OK)
			if not loan_obj:
				return Response({"message": "Loan with the loan id cannot be found"},
								status=status.HTTP_404_NOT_FOUND)

		elif decision == 'decline':
			loan_obj = Loan.objects.filter(pk=loan).first()
			if loan_obj.status == 'denied':
				return Response({'error': 'Loan has already been declined.'}, status=status.HTTP_400_BAD_REQUEST)
			loan_obj.status = 'denied'
			loan_obj.save()
			LoanApproval.objects.create(loan=the_loan, staff=staff, decision='declined')
			Loan.objects.filter(id=loan_obj.id).update(approved=False, staff_permission_accepted=False, staff_permission_approved=False)
			LoanApproval.objects.create(decision='declined', staff=staff, loan=loan_obj)
			return Response({"message": "loan has been declined"})

		return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

class EarlySettledLoans(APIView):
	def get(self, request, pk=None):
		balanced_loans = Loan.objects.filter(status = "fully paid")
		result = []
		for loan in balanced_loans:
			loan_repayments = LoanRepayment.objects.filter(loan=loan, last_repayment_date__lt = loan.maturity_date)
			for repayment in loan_repayments:
				result.append(loan)
		serializer = LoanSerializer(result, many=True)
		result = None
		return Response(serializer.data)


class DueLoansBetween(APIView):
	def get(self, request, pk=None):
		start_date = request.GET.get("start_date")
		end_date = request.GET.get("end_date")
		filtered_loans = Loan.objects.filter(maturity_date__gt = start_date).filter(maturity_date__lt = end_date)
		serializer = LoanSerializer(filtered_loans, many=True)
		result = None
		return Response(serializer.data)


class DueLoansNoPayment(APIView):
	def get(self, request, pk=None):
		filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today()).filter(amount_paid__lte = 0)
		serializer = LoanSerializer(filtered_loans, many=True)
		result = None
		return Response(serializer.data)


class DueLoansPartPayment(APIView):
	def get(self, request, pk=None):
		filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today()).filter(amount_paid__gte = 0).exclude(status= "fully paid")
		serializer = LoanSerializer(filtered_loans, many=True)
		result = None
		return Response(serializer.data)


class GetDueLoansByDays(APIView):
	def get(self, request, pk=None):
		days_due = request.GET.get("days_due")
		filtered_loans = Loan.objects.filter(maturity_date__lte = datetime.date.today())
		data = []
		for filtered_loan in filtered_loans:
			if ((datetime.date.today() - filtered_loans[0].maturity_date).days) >= int(days_due):
				data.append(filtered_loan)
		serializer = LoanSerializer(data, many=True)
		return Response(serializer.data)


class ManualRepayment(APIView):
	def post(self, request, pk=None):
		amount = int(request.data.get('amount'))
		loan = request.data.get('loan')
		repayment_mode = request.data.get('repayment_mode')
		payment_type = request.data.get('payment_type')
		proof_of_payment = request.FILES.get('proof_of_payment')
		collector = request.data.get('collector')
		comment = request.data.get('comment')
		collector = LoanOfficer.objects.get(pk = int(collector))
		sent_amount = amount
		the_loan = Loan.objects.get(pk = loan)
		try:
			if(the_loan.amount_paid == None):
				the_loan.amount_paid = 0.00
			if(the_loan.remaining_balance == 0.00):
				the_loan.status = "fully paid"
			the_loan.amount_paid += amount
			the_loan.remaining_balance -= amount
			the_loan.save()
		except:
			pass
		get_schedule = LoanScheduler.objects.filter(loan = loan).order_by("date")
		if len(get_schedule) == 0:
			return Response({"msg":"open loan found"})
		for unit in get_schedule:
			if(unit.status != "settled"):
				if(int(amount) < unit.amount):
					unit.amount -= int(amount)
					unit.paid += int(amount)
					unit.pending_due -= int(amount)
					unit.total_due -= int(amount)
					unit.principal_due -= int(amount)
					amount = 0
					unit.save()
				else:
					unit.status = "settled"
					unit.paid = unit.due
					unit.pending_due = 0
					unit.total_due = 0
					unit.principal_due = 0
					amount -= unit.amount
					unit.amount = 0
					unit.save()
			else:
				pass
		loan_payment = LoanRepayment.objects.create(
			loan=the_loan,\
			date=datetime.date.today(),\
			amount=sent_amount,\
			repayment_mode = repayment_mode,\
			payment_type = payment_type,\
			proof_of_payment = proof_of_payment,\
			collector = collector,\
			comment = comment
		)
		serializer = LoanSchedulerSerializer(get_schedule, many=True)
		return Response({"msg":"repayment was successful","schedule": serializer.data})


class AutomaticRepayment(APIView):
	#directDebit("AUTH_nbd2sdkqkb","lexmill99@gmail.com","500000")
	def post(self, request, pk=None):
		amount = int(request.data.get('amount'))
		loan = request.data.get('loan')
		comment = "Direct Debit"
		repayment_mode = "Wire Transfer"
		payment_type = "card"
		proof_of_payment = request.FILES.get('proof_of_payment')
		# collector = "Not Applicable(Automatic repayment)"
		sent_amount = amount
		the_loan = Loan.objects.get(pk = loan)
		email = the_loan.email
		if email is None:
			return Response({"msg":"pls provide an email address to continue"}, status=status.HTTP_400_BAD_REQUEST)
		if (the_loan.authorization_code == None):
			return Response({"msg":"pls register for direct debit service as you do not have an authorization code"}, status=status.HTTP_400_BAD_REQUEST)
		direct_debit_status = directDebit(the_loan.authorization_code, email , float(amount))
		if (direct_debit_status['data']['status'] != "success"):
			return Response({"msg":"pls retry with better network or verify your account has enough funds"}, status=status.HTTP_400_BAD_REQUEST)
		try:
			if(the_loan.amount_paid == None):
				the_loan.amount_paid = 0.00
			if(the_loan.remaining_balance == 0.00):
				the_loan.status = "fully paid"
			the_loan.amount_paid += amount
			the_loan.remaining_balance -= amount
			the_loan.save()
		except:
			pass
		get_schedule = LoanScheduler.objects.filter(loan = loan).order_by("date")
		if len(get_schedule) == 0:
			return Response({"msg":"open loan found"})
		for unit in get_schedule:
			if(unit.status != "settled"):
				if(int(amount) < unit.amount):
					unit.amount -= int(amount)
					unit.paid += int(amount)
					unit.pending_due -= int(amount)
					unit.total_due -= int(amount)
					unit.principal_due -= int(amount)
					if unit.principal_due < 0:
						unit.principal_due = 0
					amount = 0
					unit.save()
				else:
					unit.status = "settled"
					unit.paid = unit.due
					unit.pending_due = 0
					unit.total_due = 0
					unit.principal_due = 0
					amount -= unit.amount
					unit.amount = 0
					unit.save()
			else:
				pass
		loan_payment = LoanRepayment.objects.create(
			loan=the_loan,\
			date=datetime.date.today(),\
			amount=sent_amount,\
			repayment_mode = repayment_mode,\
			payment_type = payment_type,\
			proof_of_payment = proof_of_payment,\
			comment = comment
		)
		serializer = LoanSchedulerSerializer(get_schedule, many=True)
		return Response({"msg":"repayment was successful","schedule": serializer.data})


class SaveAuthCode(APIView):
	def post(self, request, pk=None):
		try:
			loan = request.data.get('loan')
			card_number = request.data.get('card_number')
			cvv = request.data.get('cvv')
			month = request.data.get('month')
			year = request.data.get('year')
			loan_instance = Loan.objects.get(pk = int(loan))
			if (loan_instance.email != None):
				email = loan_instance.email
			else:
				return Response({"msg":"pls provide an email address to continue"})
			#ddebitCode("lexmill99@gmail.com", "1.00", "4084084084084081", "408", "02", "22")
			auth_code = ddebitCode(email, "2500", card_number, cvv, month, year)
			loan_instance.authorization_code = auth_code
			loan_instance.save()
			return Response({"msg":"authorization code has been saved and 2500 was deducted from your account"}, status = status.HTTP_200_OK)    
		except:
			return Response({"msg":"charge was not successful, retry with enough balance and good network"}, status=status.HTTP_400_BAD_REQUEST) 



class OverrideLoanMaturity(APIView):
	def post(self, request):
		loan = request.data.get("loan")
		new_date = request.data.get('new_date')
		new_date = parse_date(new_date)
		print(new_date)
		filtered_loan = Loan.objects.get(pk=loan)
		print(filtered_loan)
		loan_schedule = LoanScheduler.objects.filter(date = filtered_loan.maturity_date).get(loan = loan)
		filtered_loan.maturity_date = new_date
		loan_schedule.date = new_date
		filtered_loan.save()
		loan_schedule.save()
		return Response({"Payment date overriden to "+str(new_date)}, status=status.HTTP_200_OK) 
 