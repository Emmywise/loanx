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
from accounting.views import CashFlowAccumlated, CashFlowMonthly
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
    CalenderEventEmailViewSet, OtherIncomeDocumentsViewSet,CollectionReport,
    OtherIncomeViewSet, OtherIncomeTypeViewSet,ReportsBetween, LoanProductReport, DisbursementReport,\
    OutstandingReport, BorrowersReport, LoanReport, LoanOfficerReport, LoanArrearsAgingReport, \
        CollectorReportStaff, FeesReport, AtAGlanceReport,
    MonthlyReport, AllEnteries
)
from loans.views import (
    LoanView, LoanCommentList, LoanCommentDetail,
    PrincipalOutstandingLoan, TotalOpenLoans, 
    InterestOutstandingLoan, FullyPaidLoans,
    LoanRepaymentViewSet, LoanCollateralViewSet,
    LoanGuarantorViewSet, GuarantorFileViewSet, LoanTypeViewSet,
    RunBvnCheck, GetLoanScore,LoanDisbursementViewSet,
    LoanOfficerList, LoanOfficerDetail,FeesOutstandingLoan,
    InterestOutstandingLoan, FullyPaidLoans, SearchLoanType, LoansByOfficers, LoanFeeList,
    LoanCollateralList, LoanCollateralDetail, LoanAttachmentList, LoanAttachmentDetail, EarlySettledLoans,
    DueLoansBetween, DueLoansNoPayment, DueLoansPartPayment, GetDueLoansByDays, OverrideLoanMaturity,
    ApproveOrDeclineLoan, ManualRepayment, SaveAuthCode, AutomaticRepayment, LoanToOfficer)
from borrowers.views import SearchBorrowerGroup, IndividualOpenLoans, BorrowersSavings, SearchByWorkingStatus,\
     IndividualRepayments
from savings_investments.views import (
    SavingsProductViewSet, SavingsAccountViewSet,
    TellerViewSet, SavingsTransactionViewSet,
    CashSourceViewSet, TransferCashViewSet,
    FundTransferLogViewSet, SavingsFeeViewSet
)
#, InitiateCreditSavings
from commons.views import (
    AssetTypeViewSet, AssetViewSet, AssetDocumentViewSet,
    AssetValuationViewSet, ExpenseTypeViewSet, ExpenseViewSet,
    ExpenseDocumentViewSet
)
from investors.views import (
    InvestorViewSet, InvestorDocumentsViewSet, InvestorInvitationViewSet,
    LoanInvestmentProductViewSet, LoanInvestmentViewSet,
    InvestorProductViewSet, InvestorAccountViewSet,
    InvestorTransactionViewSet
)

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
router.register('loan-disbursement', LoanDisbursementViewSet, 'loan-disbursement')
router.register('loan-type', LoanTypeViewSet, 'loan-type')
router.register('loan-collateral', LoanCollateralViewSet, 'loan-collateral')
router.register('loan-guarantor', LoanGuarantorViewSet, 'loan-guarantor')
router.register('loan-guarantor-file', GuarantorFileViewSet, 'loan-guarantor-file')

router.register('savings-products', SavingsProductViewSet, 'savings-products')
router.register('savings-accounts', SavingsAccountViewSet, 'savings-accounts')
router.register('teller', TellerViewSet, 'teller')
router.register('savings-transaction', SavingsTransactionViewSet, 'savings-transaction')
router.register('cash-source', CashSourceViewSet, 'cash-source')
router.register('transfer-cash', TransferCashViewSet, 'transfer-cash')
router.register('transfer-funds', FundTransferLogViewSet, 'transfer-funds')
router.register('savings-fee', SavingsFeeViewSet, 'savings-fee')

router.register('asset-type', AssetTypeViewSet, 'asset-type')
router.register('asset', AssetViewSet, 'asset')
router.register('asset-document', AssetDocumentViewSet, 'asset-document')
router.register('expense-type', ExpenseTypeViewSet, 'expense-type')
router.register('expense', ExpenseViewSet, 'expense')
router.register('asset-valuation', AssetValuationViewSet, 'asset-valuation')
router.register('expense-document', ExpenseDocumentViewSet, 'expense-document')

router.register('other-income-type', OtherIncomeTypeViewSet, 'other-income-type')
router.register('other-income', OtherIncomeViewSet, 'other-income')
router.register('other-income-document', OtherIncomeDocumentsViewSet, 'other-income-document')

router.register('investor', InvestorViewSet, 'investor')
router.register('investor-document', InvestorDocumentsViewSet, 'investor-document')
router.register('investor-invitation', InvestorInvitationViewSet, 'investor-invitation')
router.register('loan-investment-product', LoanInvestmentProductViewSet, 'loan-investment-product')
router.register('loan-investment', LoanInvestmentViewSet, 'loan-investment')
router.register('investor-product', InvestorProductViewSet, 'investor-product')
router.register('investor-account', InvestorAccountViewSet, 'investor-account')
router.register('investor-transaction', InvestorTransactionViewSet, 'investor-transaction')


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
    path('loans/', LoanView.as_view()) ,
    path('loans/<int:pk>/', LoanView.as_view()) ,
    path('principal_outstanding_loans/', PrincipalOutstandingLoan.as_view()),
    path('total_open_loan/', TotalOpenLoans.as_view()),
    path('override_maturity/', OverrideLoanMaturity.as_view()),
    path('loan_comments/', LoanCommentList.as_view()),
    path('loan_comments/<int:pk>', LoanCommentDetail.as_view()),
    path('loan_officers/', LoanOfficerList.as_view()),
    path('loan_officers/<int:pk>', LoanOfficerDetail.as_view()),
    path('loan_to_officer/', LoanToOfficer.as_view()),
    path('loan_to_officer/<int:pk>', LoanToOfficer.as_view()),
    path('interest_outstanding_loan/', InterestOutstandingLoan.as_view()),
    path('fully_paid_loan/', FullyPaidLoans.as_view()),
    path('api/bvn_check/', RunBvnCheck.as_view()),
    path('api/get_loan_score/', GetLoanScore.as_view()),
    path('search_loan_type/', SearchLoanType.as_view()),
    path('search_borrower_group', SearchBorrowerGroup),
    path('individual_open_loans', IndividualOpenLoans),
    path('individual_repayments', IndividualRepayments),
    path('fees_outstanding', FeesOutstandingLoan.as_view()),    
    path('borrowers_savings/', BorrowersSavings),
    path('search_by_working_status/<str:status>',SearchByWorkingStatus),
    path('loan_by_officer/<int:pk>', LoansByOfficers.as_view()),
    path('loan_fees/', LoanFeeList.as_view()),
    path('loan_collateral/', LoanCollateralList.as_view()),
    path('loan_collateral/<int:pk>', LoanCollateralDetail.as_view()),
    path('loan_attachment/', LoanAttachmentList.as_view()),
    path('loan_attachment/<int:pk>', LoanAttachmentDetail.as_view()),
    path('early_settled_loans/', EarlySettledLoans.as_view()),
    path('due_loans_between/',  DueLoansBetween.as_view()),
    path('due_loans_no_payment/', DueLoansNoPayment.as_view()),
    path('due_loans_part_payment/', DueLoansPartPayment.as_view()),
    path('due_loans_by_days/', GetDueLoansByDays.as_view()),
    path('api/approve-or-decline-loan/', ApproveOrDeclineLoan.as_view()),
    path('api/make_manual_repayment/', ManualRepayment.as_view()),
    path('api/save_auth_code/', SaveAuthCode.as_view()),
    path('api/make_automatic_repayment/', AutomaticRepayment.as_view()),
    path('api/cash_flow_accumulated/', CashFlowAccumlated.as_view()),
    path('api/cash_flow_monthly/', CashFlowMonthly.as_view()),
    path('api/borrowers_report/', BorrowersReport.as_view()),
    path('api/filter_borrowers_report/',ReportsBetween.as_view()),
    path('api/loans_report/',LoanReport.as_view()),
    path('api/loan_officer_report/',LoanOfficerReport.as_view()),
    path('api/loan_officer_arrears_report/',LoanArrearsAgingReport.as_view()),
    path('api/loan_product_report/',LoanProductReport.as_view()),
    path('api/collection_report/',CollectionReport.as_view()), 
    path('api/collection_report_staff/',CollectorReportStaff.as_view()),
    path('api/disbursement_report/',DisbursementReport.as_view()),  
    path('api/fees_report/',FeesReport.as_view()),    
    path('api/outstanding_report/',OutstandingReport.as_view()),     
    path('api/at_a_glance_report/',AtAGlanceReport.as_view()), 
    path('api/monthly_report/', MonthlyReport.as_view()),   
    path('api/all_enteries/', AllEnteries.as_view()),                        
    #path('api/initiate_credit_savings/', InitiateCreditSavings.as_view()),    
]

