"""loan_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework.routers import DefaultRouter
from accounts.views import (
    UserAccounts, CountryViewSet, BranchViewSet,
    BranchHolidayViewSet, BranchAdminViewSet,
    UserProfileViewSet, ResendActivationToken,
    ActivateAccount, ChangePassword,
    SendResetPassword, ConfirmResetToken,
    ResetPassword
)
from staffs.views import PayrollViewSet
from reports.views import (
    CalendarEventViewSet, CalendarLogViewSet,
    CalenderEventEmailViewSet
)
from loans.views import (
    LoanView, LoanCommentList, LoanCommentDetail,
    PrincipalOutstandingLoan, TotalOpenLoans, 
    InterestOutstandingLoan, FullyPaidLoans,
    LoanRepaymentViewSet, LoanCollateralViewSet,
    LoanGuarantorViewSet, GuarantorFileViewSet,
    RunBvnCheck, GetLoanScore,
    PrincipalOutstandingLoan, TotalOpenLoans, LoanOfficerList, LoanOfficerDetail,
    InterestOutstandingLoan, FullyPaidLoans, SearchLoanType, LoansByOfficers
    )
from borrowers.views import SearchBorrowerGroup, IndividualOpenLoans, BorrowersSavings, SearchByWorkingStatus


router = DefaultRouter()

router.register('accounts', UserAccounts, 'accounts')
router.register('country', CountryViewSet, 'country')
router.register('branch', BranchViewSet, 'branch')
router.register('branch-holiday', BranchHolidayViewSet, 'branch-holiday')
router.register('branch-admin', BranchAdminViewSet, 'branch-admin')
router.register('user-profile', UserProfileViewSet, 'user-profile')
router.register('calendar-events', CalendarEventViewSet, 'calendar-events')
router.register('calendar-logs', CalendarLogViewSet, 'calendar-logs')
router.register('calendar-events-email', CalenderEventEmailViewSet, 'calendar-events-email')

router.register('payroll', PayrollViewSet, 'payroll')

router.register('loan-repayment', LoanRepaymentViewSet, 'loan-repayment')
router.register('loan-collateral', LoanCollateralViewSet, 'loan-collateral')
router.register('loan-guarantor', LoanGuarantorViewSet, 'loan-guarantor')
router.register('loan-guarantor-file', GuarantorFileViewSet, 'loan-guarantor-file')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_jwt_token),
    path('api-verify-auth/', verify_jwt_token),
    path('api/resend-activation-token/', ResendActivationToken.as_view()),
    path('api/activate-account/', ActivateAccount.as_view()),
    path('api/change-password/', ChangePassword.as_view()),
    path('api/send-reset-password/', SendResetPassword.as_view()),
    path('api/confirm-reset-token/', ConfirmResetToken.as_view()),
    path('api/reset-password/', ResetPassword.as_view()),
    path('notifications/', include('notifications.urls')) ,
    path('borrowers/', include('borrowers.urls')) ,
    path('borrowers_group/', include('borrowers.urls')) ,
    path('loans/', LoanView.as_view()) ,
    path('principal_outstanding_loan/', PrincipalOutstandingLoan.as_view()),
    path('total_open_loan/', TotalOpenLoans.as_view()),
    path('loan_comments/', LoanCommentList.as_view()),
    path('loan_comments/<int:pk>', LoanCommentDetail.as_view()),
    path('loan_officers/', LoanOfficerList.as_view()),
    path('loan_officers/<int:pk>', LoanOfficerDetail.as_view()),
    path('interest_outstanding_loan/', InterestOutstandingLoan.as_view()),
    path('fully_paid_loan/', FullyPaidLoans.as_view()),
    path('api/bvn_check/', RunBvnCheck.as_view()),
    path('api/get_loan_score/', GetLoanScore.as_view()),
    path('search_loan_type/', SearchLoanType.as_view()),
    path('search_borrower_group', SearchBorrowerGroup),
    path('individual_open_loans', IndividualOpenLoans),
    path('borrowers_savings/', BorrowersSavings),
    path('search_by_working_status/<str:status>',SearchByWorkingStatus),
    path('loan_by_officer/<int:pk>', LoansByOfficers.as_view()),


]

