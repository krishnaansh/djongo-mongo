
"""
Common Utility Method
"""

# python import
import re
from datetime import datetime, timedelta

# third party imports
from django.contrib.auth import get_user_model
from oauth2_provider.models import AccessToken
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

# local import
from oauthlib.common import generate_token
from odata.utility.messages import ERROR_CODE
from odata.utility.constant import SPECIAL_CHARACTERS, INT_NUMBER
from odata.utility import messages as util_message
from oauth2_provider.models import Application, AccessToken, RefreshToken

USER = get_user_model()

def get_message(obj):
    """

    :param obj:
    :return:
    """
    result = None
    if isinstance(obj, list):
        if isinstance(obj[0], list):
            result = get_message(obj[0][0])
        elif isinstance(obj[0], dict):
            result = get_message(obj[0].items()[0])
        else:
            result = obj[0]

    elif isinstance(obj, dict):
        dict_item = list(obj.items())
        if isinstance(dict_item, dict):
            result = get_message(dict_item.items()[0])
        elif isinstance(dict_item, list):
            result = get_message(dict_item[0])
        else:
            result = dict_item

    elif isinstance(obj, tuple):
        result = get_message(obj[1])

    return result


class ApiResponse:
    """
        Api response class
    """
    is_success = False
    is_error = False
    is_validation_error = False

    def custom_response(self, message=None, data=None, response_status=status.HTTP_200_OK, allow_empty_list=False):
        """
        Custom Response
        :return:
        """
        self.is_success = True
        if allow_empty_list:
            response = Response({"detail": message if message else util_message.SUCCESS_CODE['3000'],
                                 "data": data}, status=response_status)
        else:
            response = Response({"detail": message if message else util_message.SUCCESS_CODE['3000'],
                                 "data": data if data else {}}, status=response_status)
        return response

    @staticmethod
    def _get_validate_error_string(errors):
        """
        To Get string for error list
        :param errors: list
        :return: string
        """
        detail_error = list(errors.values())[0]
        if isinstance(detail_error, list):
            detail_error = detail_error[0]
        if isinstance(detail_error, dict):
            detail_error = list(detail_error.values())[0]
        return detail_error

    def custom_error(self, message=None, response_status=status.HTTP_400_BAD_REQUEST):
        """
        Custom Error
        :return:
        """
        self.is_error = True
        error = message
        if isinstance(message, str):
            error = None
        else:
            message = self._get_validate_error_string(error)
        return Response({"detail": message, "error": error}, status=response_status)

    def custom_validate_error(self, message=None):
        """
        :param message: error message
        :return:
        """
        self.is_validation_error = True
        raise ValidationError({'detail': message})

def logout(user_id, access_token):
    """
    remove access_token and registration_token
    """
    try:        
        user = USER.objects.get(pk=user_id)        
        user.oauth2_provider_accesstoken.filter(token=access_token).delete()        
    except USER.DoesNotExist:
        pass


def expire_previous_tokens(user_id):
    """
    remove access_token and registration_token
    """
    AccessToken.objects.filter(user_id=user_id).delete()

def get_access_token(user):
    """
    :param user: account instance
    :return: access-token in json format
    """
    app, created = Application.objects.get_or_create(user=user)
    if created:
        user.last_login = None
    else:
        user.last_login = datetime.now()
        user.save()
    token = generate_token()
    refresh_token = generate_token()
    expire_time = 500
    expires = datetime.now() + timedelta(days=expire_time)
    scope = "read write"
    access_token_instance = AccessToken.objects.create(user=user,
                                                       application=app,
                                                       expires=expires,
                                                       token=token,
                                                       scope=scope)
    RefreshToken.objects.create(user=user,
                                application=app,
                                token=refresh_token,
                                access_token=access_token_instance)
    token_json = {
        'access_token': token,
        'expires_in': expire_time,
        'refresh_token': refresh_token,
        'scope': scope
    }
    return token_json

def validate_password(password):
    """
    Method to validate account password
    """
    regex = re.compile(SPECIAL_CHARACTERS)
    if len(password) < INT_NUMBER['EIGHT']:
        raise serializers.ValidationError(
            ERROR_CODE['password']['character_limit'])
    elif re.search('[0-9]', password) is None:
        raise serializers.ValidationError(
            ERROR_CODE['password']['number_required'])
    elif re.search('[A-Z]', password) is None:
        raise serializers.ValidationError(
            ERROR_CODE['password']['capital_letter_required'])
    elif re.search('[a-z]', password) is None:
        raise serializers.ValidationError(
            ERROR_CODE['password']['small_letter_required'])
    elif regex.search(password) is None:
        raise serializers.ValidationError(
            ERROR_CODE['password']['special_character_required'])
    elif ' ' in password:
        raise serializers.ValidationError(
            ERROR_CODE['global_error']['not_allowed'].format(
                "spaces", "password"))

    return password

def validate_name(names):
    """
    Method to validate name
    """
    for name in names:
        if re.search('[0-9]', name):
            raise serializers.ValidationError(
                ERROR_CODE['global_error']['not_allowed'].format(
                    "numbers", "both first name and last name"))
    return names
