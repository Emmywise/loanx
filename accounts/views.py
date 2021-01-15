import string
import random
from django.utils import timezone
from django.db.models import Q
import datetime
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Profile, Country, Branch, BranchHoliday, BranchAdmin,
    AccountResetLink, SuspendedAccount
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .serializers import (
    UserSerializer, CountrySerializer, BranchSerializer,
    BranchSerializer2, UserSuspendSerializer,
    BranchHolidaySerializer, BranchAdminSerializer,
    UserProfileSerializer, SuspendAccountSerializer 
)
from staffs.models import Staff
from loan_management_system import permissions as perms


# Create your views here.


def generate_token():
    token = ''
    for i in range(50):
        token += random.choice(string.ascii_letters +
                               string.digits + string.hexdigits)
    return token


def set_activation_token():
    token = generate_token()
    while Profile.objects.filter(activation_token=token).first():
        token = generate_token()
    return token


def send_activation_token(user, profile):
    if not profile.activation_token:
        profile.activation_token = set_activation_token()
        profile.save()
    subject, from_email, to = 'Activate your account', \
                              'admin@lms.com.ng', user.email
    text_content = 'Hey {} please reset password'.format(user.username)
    html_content = '<p>Hey {a} please reset password .' \
                   '</p><a href="https://localhost:8000.com.ng/reset-password/{b}">' \
                   'https://holidaypro.com.ng/reset-password/{b}</a>' \
        .format(a=user.username, b=profile.activation_token)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class UserAccounts(viewsets.ViewSet):

    def create(self, request):
        check_branch = Branch.objects.filter(id=request.data['branch']).exists()
        if check_branch:
            get_branch = Branch.objects.get(id=request.data['branch'])
        if get_branch.is_open == False:
            return Response({"Error": "Selected Branch is not open or closed. Choose an opened Branch or open a Branch for this user."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=serializer.data['id'])
            send_activation_token(user, user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        serializer = UserSerializer(data=request.data, partial=True)
        try:
            user = User.objects.get(pk=pk)
            if serializer.is_valid():
                serializer.update(user, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as err:
            print(err)
            return Response({"message": "user does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer

    def get_queryset(self):
        queryset = Branch.objects.all()

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = BranchSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

# class BranchViewSet(viewsets.ModelViewSet):
#     serializer_class = BranchSerializer

#     def get_queryset(self):
#         queryset = Branch.objects.all()

#         return queryset


class BranchHolidayViewSet(viewsets.ModelViewSet):
    serializer_class = BranchHolidaySerializer

    def get_queryset(self):
        queryset = BranchHoliday.objects.all()

        return queryset


class BranchAdminViewSet(viewsets.ModelViewSet):
    serializer_class = BranchAdminSerializer

    def get_queryset(self):
        queryset = BranchAdmin.objects.all()
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch__pk=branch)
        return queryset


class UserProfileViewSet(viewsets.ModelViewSet):

    permission_classes = (perms.IsOwnerOrStaffOrAdmin,)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = User.objects.filter(profile__isnull=False)
        # username, first_name, last_name, active, branch,
        # user_type, is_super_admin,
        # filter by loan officer
        params = self.request.GET
        username = params.get('username')
        first_name = params.get('first_name')
        last_name = params.get('last_name')
        active = params.get('active')
        branch = params.get('branch')
        user_type = params.get('user_type')
        super_admin = params.get('super_admin')
        if username:
            queryset = queryset.filter(username=username)
        if first_name:
            queryset = queryset.filter(first_name=first_name)
        if last_name:
            queryset = queryset.filter(last_name=last_name)
        if active and (active == 'true'):
            print(active)
            queryset = queryset.filter(profile__active=True)
        if active and (active == 'false'):
            queryset = queryset.filter(profile__active=False)
        if branch:
            queryset = queryset.filter(profile__branch__pk=branch)
        if user_type:
            queryset = queryset.filter(profile__user_type=user_type)
        if super_admin and (super_admin == 'true'):
            queryset = queryset.filter(profile__is_super_admin=True)

        return queryset

class UserSuspension(viewsets.ViewSet):

    def partial_update(self, request, pk=None):
        serializer = UserSuspendSerializer(data=request.data, partial=True)
        try:
            user = Profile.objects.get(pk=pk)
            if serializer.is_valid():
                serializer.update(user, serializer.validated_data)
                if serializer.validated_data['suspend'] == True:
                    SuspendedAccount.objects.get_or_create(profile=user)
                else:
                    SuspendedAccount.objects.filter(profile=user).update(status=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as err:
            print(err)
            return Response({"message": "user does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

class SuspendAccountView(APIView):

    def get(self, request, pk=None):
        get_suspended_account = SuspendedAccount.objects.all()
        serializer = SuspendAccountSerializer(get_suspended_account, many=True)
        return Response(serializer.data)





class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.data)
        element_counter = 0
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if user_id:
            element_counter += 1
        if old_password:
            element_counter += 1
        if new_password:
            element_counter += 1
        if element_counter != 3:
            return Response({"message": "element required for the request is missing"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password changed successful"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "old password does not match"},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "User not found"})


class ResendActivationToken(APIView):

    def post(self, request):
        email = request.data.get("email")

        errors = []

        if not email:
            errors.append(dict(email='email field is required'))

        if len(errors) > 0:
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)
            send_activation_token(user, profile)
            return Response({"message": "activation token resent to your email"},
                            status=status.HTTP_200_OK)
        except:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccount(APIView):

    def post(self, request):
        email = request.data.get("email")
        token = request.data.get("token")

        errors = []

        if not email:
            errors.append(dict(email='email field is required'))

        if not token:
            errors.append(dict(token='token field is required'))

        if len(errors) > 0:
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)
            if token == profile.activation_token:
                profile.active = True
                profile.save()
                return Response({"message": "account has been activated successful"},
                                status=status.HTTP_200_OK)
            return Response({"message": "invalid activation token"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class SendResetPassword(APIView):

    def get_user_or_none(self, email):
        user = User.objects.filter(email=email).first()
        return user

    def get_link(self, user):
        link = AccountResetLink.objects.filter(user=user).first()
        if not link:
            link = AccountResetLink.objects.create(user=user)
        else:
            if timezone.now() > (link.date_time + datetime.timedelta(hours=2)):
                print('Current time is 2mins ahead of expiry date')
                link.delete()
                link = AccountResetLink.objects.create(user=user)
                return link
        return link

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "email field is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_user_or_none(email)
        if user:
            link = self.get_link(user)
            subject, from_email, to = 'Reset password from Holidaypro', 'admin@holidaypro.com.ng', email
            text_content = 'Hey {} please reset password'.format(user.username)
            html_content = '<p>Hey {a} please reset password .' \
                           '</p><a href="https://holidaypro.com.ng/reset-password/{b}">' \
                           'https://holidaypro.com.ng/reset-password/{b}</a>' \
                .format(a=user.username, b=link.reset_token)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response({"message": "Reset link has been sent to your account"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetToken(APIView):

    def post(self, request):
        token = request.data.get("reset_token")
        if not token:
            return Response({"token": "reset token is required"}, status=status.HTTP_400_BAD_REQUEST)
        reset_link = AccountResetLink.objects.filter(reset_token=token).first()
        if reset_link:
            if timezone.now() <= (reset_link.date_time + datetime.timedelta(minutes=5)):
                return Response({"message": "reset token is valid"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "reset token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):

    def post(self, request):
        token = request.data.get("reset_token")
        password = request.data.get("password")
        errors = []
        if not token:
            errors.append({"token": "reset token is required"})
        if not password:
            errors.append({"password": "new password is required"})
        if len(errors) > 0:
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)

        reset_link = AccountResetLink.objects.filter(reset_token=token).first()
        if not reset_link:
            return Response({"message": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() <= (reset_link.date_time + datetime.timedelta(hours=2)):
            user = reset_link.user
            user.set_password(password)
            user.save()
            return Response({"message": "password changed successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Reset token has expired"})


def jwt_response_payload_handler(token, user=None, request=None):
    profile = Profile.objects.get(user=user)
    if profile.user_type == 'staff':
        staff = Staff.objects.get(user_id=profile.id)
        staff_name = staff.user_id.user.first_name + ' ' + staff.user_id.user.last_name
        return dict(token=token, userid=user.id, staff_id=staff.id, staff_name=staff_name)
    else:
        return dict(token=token, userid=user.id)
