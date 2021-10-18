"""
    Custom validators
"""

from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from odata.utility.messages import ERROR_CODE


class CustomValidation(APIException):
    """
        Custom Validator for raising exception in same manner(used whole application).
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ERROR_CODE['global_error']['something_wrong']

    def __init__(self, detail, status_code, field='detail'):
        """
        :param detail:
        :param field:
        :param status_code:
        """
        if status_code is not None:
            self.status_code = status_code

        if detail is not None:
            self.detail = {field: force_text(detail)}
        else:
            self.detail = {'detail': force_text(self.default_detail)}


USER_UNIQUE_FIELD_VALIDATOR = [
    UniqueTogetherValidator(
        queryset=User.objects.all(),
        fields=['email'],
        message=ERROR_CODE['user']['already_register']
    ),
   
]
