"""Accounts auth API"""

# third party import
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

# local import
from odata.utility.helpers import ApiResponse, get_message, logout
from odata.utility.messages import ERROR_CODE, SUCCESS_CODE
from odata.serializers.auth_serializer import (
    LoginSerializer,
    CustomerRegistrationSerializer,
    UserForgotPasswordSerializer,
    VerifyUserForgotPasswordSerializer,
    ResetPasswordSerializer
)


class LoginViewSet(viewsets.ModelViewSet, ApiResponse):
    """
    Login Model View-set
    """

    serializer_class = LoginSerializer
    queryset = User.objects.all()
    http_method_names = ["post"]

    def get_serializer_context(self):
        """
        Serializer Context
        :return: context
        """
        return {"request": self.request}


class LogoutViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, ApiResponse):
    """
    Logout view is used for user logout.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = None
    http_method_names = ("post",)

    def create(self, request, *args, **kwargs):
        """
        :param request: request user
        :param args: argument list
        :param kwargs: keyword argument object
        :return: logout a user
        """        
        logout(request.user.id, request.META["HTTP_AUTHORIZATION"].split(" ")[1])
        return self.custom_response(
            message=SUCCESS_CODE["user"]["log_out"],
            data=None,
            response_status=status.HTTP_200_OK,
        )


class SignupViewSet(viewsets.ModelViewSet, ApiResponse):
    """
    Signup ViewSet for customers
    """

    queryset = User.objects.all()
    serializer_class = CustomerRegistrationSerializer
    http_method_names = ("post",)

    def create(self, request, **kwargs):
        """
            Creating a customer
        :param request: wsgi request
        :param kwargs: allows for any number of keyword arguments (parameters) which will be dict named keyword
        :return: Created user instance

        signup request body
        {
        "first_name" : "test",
        "last_name" : "test",
        "email" : "test@yopmail.com",
        "password" : "Qwerty@1",
        }

        """

        user_create_serializer_instance = self.serializer_class(
            data=request.data,
            context={"confirm_password": request.data.get("confirm_password")},
        )
        if user_create_serializer_instance.is_valid():
            user_create_serializer_instance.save()
            return self.custom_response(
                SUCCESS_CODE["user"]["registration_done"],
                user_create_serializer_instance.data,
                response_status=status.HTTP_201_CREATED,
            )

        return self.custom_error(
            get_message(user_create_serializer_instance.errors),
            response_status=status.HTTP_400_BAD_REQUEST,
        )


class UserForgotPasswordViewSet(viewsets.GenericViewSet, ApiResponse):
    """
    forgot password
    """

    serializer_class = UserForgotPasswordSerializer
    http_method_names = ("post",)

    def create(self, request):
        forgot_password_serializer = self.serializer_class(data=request.data)
        if forgot_password_serializer.is_valid():
            forgot_password_serializer.save()
            return self.custom_response(
                SUCCESS_CODE["3000"],
                data=forgot_password_serializer.data,
                response_status=status.HTTP_200_OK,
            )
        return self.custom_error(
            list(forgot_password_serializer.errors.values())[0][0],
            status.HTTP_400_BAD_REQUEST,
        )


class VerifyUserForgotPasswordViewSet(viewsets.GenericViewSet, ApiResponse):
    """
    forgot password
    """

    serializer_class = VerifyUserForgotPasswordSerializer
    http_method_names = ("post",)

    def create(self, request):
        verify_forgot_password_serializer = self.serializer_class(data=request.data)
        if not verify_forgot_password_serializer.is_valid():
            return self.custom_error(
                get_message(verify_forgot_password_serializer.errors),
                status.HTTP_400_BAD_REQUEST,
            )

        verify_forgot_password_serializer.save()
        return self.custom_response(
            SUCCESS_CODE["user"]['verify_forgot_password'], data={}, response_status=status.HTTP_200_OK
        )


class ResetPasswordViewSet(viewsets.GenericViewSet, ApiResponse):
    """
    Class to reset password
    """
    serializer_class = ResetPasswordSerializer
    http_method_names = ('post',)

    def create(self, request):
        reset_password_serializer = self.serializer_class(data=request.data)
        if not reset_password_serializer.is_valid():
            return self.custom_error(get_message(reset_password_serializer.errors),
                                     status.HTTP_400_BAD_REQUEST
                                     )

        reset_password_serializer.save()
        return self.custom_response(SUCCESS_CODE["user"]["reset_password"], data={},
                                    response_status=status.HTTP_200_OK)
