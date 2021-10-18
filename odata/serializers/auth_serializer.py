"""Auth Serializer"""

# third party imports
import re, random
from datetime import datetime

from django.db.models import Q
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.models import User

from rest_framework import exceptions
from rest_framework import serializers

# local imports
from odata.models import UserForgotPassword, Customer
from odata.utility.constant import SPECIAL_CHARACTERS
from odata.utility.validator import USER_UNIQUE_FIELD_VALIDATOR
from odata.utility.messages import ERROR_CODE, ErrorManager, SUCCESS_CODE
from odata.utility.helpers import (
    ApiResponse,
    get_access_token,
    validate_password,
    validate_name,
)


class LoginSerializer(serializers.ModelSerializer, ApiResponse):
    """
    Serializer for login process.
    """

    email = serializers.EmailField(
        required=True,
        error_messages={"blank": ErrorManager().get_blank_field_message("email")},
    )
    password = serializers.CharField(
        max_length=100,
        required=True,
        trim_whitespace=False,
        error_messages={"blank": ErrorManager().get_blank_field_message("password")},
    )
    token = serializers.SerializerMethodField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        """
        Meta class for serializer
        """

        model = User
        fields = ("id", "email", "password", "token", "first_name", "last_name")

    def validate_data(self, validated_data):
        """

        :param validated_data:
        :return:
        """
        email = validated_data.get("email", None)
        password = validated_data.get("password", None)

        try:
            user = User.objects.get(Q(email__iexact=email) | Q(username__iexact=email))
        except User.DoesNotExist:
            self.custom_validate_error(message=ERROR_CODE["user"]["not_exist"])

        if not user.is_active:
            self.custom_validate_error(message=ERROR_CODE["login"]["deactive"])

        if not user.check_password(password):
            self.custom_validate_error(
                message=ERROR_CODE["login"]["invalid_credential"]
            )

        return user

    def create(self, validated_data):
        """

        :param validated_data:
        :return:
        """
        user = self.validate_data(validated_data)
        return user

    @staticmethod
    def get_token(obj):
        """
        Get token
        :return:
        """
        return get_access_token(obj)

    def to_representation(self, obj):
        """
        get the original representation
        :param obj: account instance
        :return: modified account instance
        """
        attr = super(LoginSerializer, self).to_representation(obj)
        attr.pop("password")
        return attr


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    first_name = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            "blank": ErrorManager().get_blank_field_message("first_name"),
            "max_length": ErrorManager().get_maximum_limit_message("first_name", "50"),
        },
    )
    last_name = serializers.CharField(
        required=True,
        max_length=50,
        error_messages={
            "blank": ErrorManager().get_blank_field_message("last_name"),
            "max_length": ErrorManager().get_maximum_limit_message("first_name", "50"),
        },
    )
    email = serializers.EmailField(
        required=True,
        max_length=150,
        min_length=5,
        error_messages={
            "blank": ErrorManager().get_blank_field_message("Email"),
            "max_length": ErrorManager().get_maximum_limit_message("Email", "150"),
            "min_length": ErrorManager().get_minimum_limit_message("Email", "5"),
            "invalid": ERROR_CODE["sign_up"]["invalid_email"],
        },
    )
    password = serializers.CharField(
        required=True,
        max_length=15,
        min_length=8,
        error_messages={
            "blank": ErrorManager().get_blank_field_message("password"),
            "min_length": ErrorManager().get_minimum_limit_message("password", "8"),
            "max_length": ErrorManager().get_maximum_limit_message("password", "15"),
        },
    )
    confirm_password = serializers.CharField(
        max_length=15,
        min_length=8,
        error_messages={
            "blank": ErrorManager().get_blank_field_message("password"),
            "min_length": ErrorManager().get_minimum_limit_message("password", "8"),
            "max_length": ErrorManager().get_maximum_limit_message("password", "15"),
        },
        read_only=True,
    )

    class Meta:
        """
        Meta class for serializer
        """

        model = User
        fields = ("first_name", "last_name", "email", "password", "confirm_password")
        validators = USER_UNIQUE_FIELD_VALIDATOR

    @staticmethod
    def validate_email(value):
        """
        validate email
        :param value: email
        :return: validated email
        """
        return value.lower()

    @staticmethod
    def validate_password(password):
        """
        Method to validate user password
        """
        return validate_password(password)

    def validate(self, data):
        """

        :param data: obj
        :return: data
        """
        if data.get("password") != self.context.get("confirm_password"):
            raise serializers.ValidationError(
                ERROR_CODE["password"]["confirm_password_invalid"]
            )
        regex = re.compile(SPECIAL_CHARACTERS)
        validate_name([data.get("first_name"), data.get("last_name")])

        return data

    @staticmethod
    def create(validated_data):
        """
            Method to create user
        :param validated_data: ordered dict that has key - value pair of account attribute
        :return: create account instance
        """
        with transaction.atomic():
            validated_data["is_active"] = True
            validated_data["username"] = validated_data["email"]
            instance = User.objects.create(**validated_data)
            instance.set_password(validated_data["password"])
            instance.save()
            Customer.objects.create(
                user=instance,
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
            )

        return instance

    def to_representation(self, instance):
        rep = super(CustomerRegistrationSerializer, self).to_representation(instance)
        rep.pop("password")
        return rep


class UserForgotPasswordSerializer(serializers.Serializer):
    """
    forgot password serializer.
    """

    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        """

        :param validated_data: data to be validated data.
        :return:
        """
        try:
            user_obj = User.objects.get(email=validated_data["email"])
            if not user_obj.is_active:
                raise exceptions.ValidationError(
                    {"detail": ERROR_CODE["user"]["inactive_user"]}
                )
        except User.DoesNotExist:
            raise exceptions.ValidationError(
                {"detail": ErrorManager().get_not_exist_message("Email")}
            )
        # create a forgot password instance and set is_consumed false.
        try:
            forgot_pass_token = UserForgotPassword.objects.get(user=user_obj)
            forgot_pass_token.delete()
        except UserForgotPassword.DoesNotExist:
            pass
        # the nosec comment is for bandit - see issue #25
        # TL;DR pseudo-random generator is unsafe for crypto use but OK here

        token = "".join([str(random.randrange(9)) for _ in range(4)])  # nosec
        UserForgotPassword.objects.create(user=user_obj, is_consumed=False, token=token)
        subject = "Forgot Password Verification"
        message = SUCCESS_CODE["user"]["verification_otp"].format(
            "Forgot password", token
        )
        email_from = settings.EMAIL_HOST_USER
        email_to = [user_obj.email,]
        send_mail(subject, message, email_from, email_to)
        return user_obj


class VerifyUserForgotPasswordSerializer(serializers.Serializer):
    """
    forgot password serializer.
    """

    token = serializers.CharField(max_length=10, required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        """

        :param validated_data:
        :return:
        """
        token = validated_data.pop("token")
        try:
            user_obj = User.objects.get(email=validated_data["email"])
            if not user_obj.is_active:
                raise exceptions.ValidationError(
                    {"detail": ERROR_CODE["user"]["inactive_user"]}
                )
        except User.DoesNotExist:
            raise exceptions.ValidationError(
                {"detail": ErrorManager().get_not_exist_message("Email")}
            )

        try:
            reset_password_instance = UserForgotPassword.objects.get(
                token=token,
                user__is_active=True,
                is_consumed=False,
                user=user_obj                
            )
        except UserForgotPassword.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": ERROR_CODE["password"]["invalid_otp"]}
            )

        return reset_password_instance


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Reset password serializer.
    """

    token = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(
        max_length=200,
        required=True,
        error_messages={"blank": ErrorManager().get_blank_field_message("password")},
    )
    confirm_password = serializers.CharField(
        required=True,
        error_messages={
            "blank": ErrorManager().get_blank_field_message("confirm password")
        },
    )

    class Meta:
        """
        Meta Class
        """

        model = User
        fields = ["token", "password", "confirm_password"]

    def validate_password(self, password):
        """
        Method to validate password
        """
        return validate_password(password)

    def create(self, validated_data):
        """

        :param validated_data:
        :return:
        """
        token = validated_data.pop("token")
        password = validated_data.pop("password")
        if not token:
            serializers.ValidationError(
                {"detail": ERROR_CODE["global_error"]["blank_field"].format("otp")}
            )
        try:
            reset_password_instance = UserForgotPassword.objects.get(
                token=token, user__is_active=True, is_consumed=False
            )
        except UserForgotPassword.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": ERROR_CODE["global_error"]["invalid"].format("otp")}
            )

        if password != validated_data.get("confirm_password"):
            raise serializers.ValidationError(
                {"details": ERROR_CODE["password"]["confirm_password_invalid"]}
            )
        reset_password_instance.is_consumed = True
        reset_password_instance.save()

        reset_password_instance.user.set_password(password)
        reset_password_instance.user.save()

        return {"token": token, "password": password}
