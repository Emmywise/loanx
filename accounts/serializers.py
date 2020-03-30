from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Branch, BranchAdmin, BranchHoliday, Country
from django.core.exceptions import ObjectDoesNotExist


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = '__all__'


class BranchHolidaySerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchHoliday
        fields = '__all__'


class BranchAdminSerializer(serializers.ModelSerializer):
    admin_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = BranchAdmin
        fields = '__all__'

    def get_admin_name(self, obj):
        return obj.admin.user.username

    def get_branch_name(self, obj):
        return obj.branch.name


class UserSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField(max_length=125, required=False)
    email = serializers.EmailField(max_length=125, required=False)
    first_name = serializers.CharField(max_length=125, required=False)
    last_name = serializers.CharField(max_length=125, required=False)
    password = serializers.CharField(max_length=125, required=False)
    user_type = serializers.ChoiceField(choices=Profile.user_type_choices, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    active = serializers.BooleanField(default=False, required=False)
    is_super_admin = serializers.BooleanField(default=False, required=False)
    branch = serializers.IntegerField(required=False)

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
            raise serializers.ValidationError("user with the username already exist")
        except ObjectDoesNotExist:
            pass
        return value

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
            raise serializers.ValidationError("user with the email already exist")
        except ObjectDoesNotExist:
            pass
        return value

    def validate_phone(self, value):
        try:
            Profile.objects.get(phone=value)
            raise serializers.ValidationError("user with the phone already exist")
        except ObjectDoesNotExist:
            pass
        return value

    def validate_branch(self, value):
        try:
            Branch.objects.get(pk=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("branch does not exist.")
        return value

    def create(self, validated_data):
        branch_id = validated_data.get('branch')
        password = validated_data.get('password')
        branch = Branch.objects.get(
            id=branch_id
        )
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        user.set_password(raw_password=password)
        user.save()
        profile = Profile.objects.create(
            user=user,
            user_type=validated_data.get('user_type'),
            phone=validated_data.get('phone'),
            active=validated_data.get('active'),
            is_super_admin=validated_data.get('is_super_admin'),
            branch=branch
        )
        return {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_type': profile.user_type,
            'phone': profile.phone,
            'active': profile.active,
            'branch': profile.branch.id,
            'is_super_admin': profile.is_super_admin
        }

    def check_value(self, key):
        if key in self.validated_data:
            return True
        return False

    def update(self, instance, validated_data):
        branch_id = validated_data.get('branch')
        branch = Branch.objects.get(
            id=branch_id
        )
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile.branch = branch
        instance.profile.user_type = validated_data.get('user_type', instance.profile.user_type)
        instance.profile.is_super_admin = validated_data.get('is_super_admin', instance.profile.is_super_admin)
        instance.profile.phone = validated_data.get('phone', instance.profile.phone)
        try:
            if validated_data['password']:
                instance.set_password(validated_data['password'])
        except:
            pass
        instance.profile.save()
        instance.save()
        return instance

    def get_id(self, validated_data):
        return validated_data['id']


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    branch_currency = serializers.SerializerMethodField()
    branch_mobile = serializers.SerializerMethodField()
    is_super_admin = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = User

    def get_phone(self, obj):
        return obj.profile.phone

    def get_active(self, obj):
        return obj.profile.active

    def get_branch_name(self, obj):
        return obj.profile.branch.name

    def get_branch_currency(self, obj):
        return obj.profile.branch.currency

    def get_branch_mobile(self, obj):
        return obj.profile.branch.mobile

    def get_is_super_admin(self, obj):
        return obj.profile.is_super_admin
