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

router = DefaultRouter()

router.register('accounts', UserAccounts, 'accounts')
router.register('country', CountryViewSet, 'country')
router.register('branch', BranchViewSet, 'branch')
router.register('branch-holiday', BranchHolidayViewSet, 'branch-holiday')
router.register('branch-admin', BranchAdminViewSet, 'branch-admin')
router.register('user-profile', UserProfileViewSet, 'user-profile')

router.register('payroll', PayrollViewSet, 'payroll')


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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', include('notifications.urls')) ,
    path('borrowers/', include('borrowers.urls')) ,
]

