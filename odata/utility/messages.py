"""
    this module contains error and success code messages.
"""

ERROR_CODE = {    
    "user": {
        "not_exist": "User doesn't exist.",
        "inactive_user": "Your account is inactive.",
        "already_register": "This email is already registered.",
        "user_name_exists": "User with this user name already exists. ",
        "not_verified": "Account is not verified.",
        "contact_administrator": "Sorry! Please contact with administrator.",
        "wrong_number": "The 'To' number {0} is not a valid phone number.",
        "contact_no_required": "Contact Number & Country code both are mandatory.",
        "already_verified": "This contact number is already verified",
        "card_inactive": "You can not deleted this card!",
    },

    "login": {
        "invalid_credential": "Invalid login credentials.",
        "invalid_password": "password should not contain any space.",
        "invalid_email": "This Email id is not registered with us",
        "invalid_contact_number": "This contact number is not registered with us",
        "wrong_password": "Please provide correct password",
        "invalid_otp": "Otp is invalid or expired.",
        "deactive": "Admin has deactivated your account."
    },

    "sign_up": {
        "user_type_required": "User Type is required in user creation.",
        "invalid_email": 'Please enter valid email id.',
        "invalid_dob": "Dob can not be grater than or equal to today's date.",
        "contact_already_exists": "User with this contact number is already registerd."
    },

    "global_error": {
        "something_wrong": "Something went wrong, please try again.",
        "invalid_data": "Invalid Data",
        "connection_error": "Connection Error",
        "invalid_id": "Invalid Id",
        "match_not_found": "No match found",
        "invalid_access_token": "Invalid access token",
        "minimum_character": "Minimum {} character required in {} field.",
        "minimum_digit": "Minimum {} digit required in {} field.",
        "wrong_order_params": "Please provide correct ordering options.",
        "invalid_date_range": "Please send correct date range",
        "invalid_permission": "You don't have permission.",
        "maximum_length": "{} should be less than {} characters.",
        "maximum_digit": "{} should be less than {} digits.",
        "does_not_exist": "{} does not exist.",
        "not_allowed": "{} not allowed in {}.",
        "invalid": "Please enter valid {}.",
        "blank_field": "{} cannot be blank.",
        "required": "{} required.",
    },
    "password": {
        "invalid_token": "Reset password token is invalid.",
        "invalid_otp": "Your OTP is Incorrect.",
        "reset": "Password has been successfully reset",
        "character_limit": "Make sure your password is at lest 8 letters",
        "number_required": "Make sure your password has a number in it.",
        "capital_letter_required": "Make sure your password has a capital letter in it.",
        "special_character_required": "Make sure password has special character in it eg(@_!#$).",
        "small_letter_required": "Make sure your password has a small letter in it.",
        "confirm_password_invalid": "Your password and confirmation password do not match",
        "reset_token_expired": "Your token is expired",
        "reset_token_invalid": "Token is invalid.",
    },
    "change_password": {
        "invalid_new_password": "Current password and new password cannot be same.",
        "invalid_current_password": "Current password didn't match.",
    },
}

# success codes for responses

SUCCESS_CODE = {
    "user": {
        "registration_done": "User has been registered successfully.",
        "updated_email": "Email has been successfully Updated.",
        "log_out": "You have successfully logged out.",
        "log_in": "You have successfully logged in.",
        "code_sent": "Unique code has been sent successfully.",
        "reset_password": "Password has been successfully reset.",
        "verification_otp": "Verification otp for {} process is {}",
        "password_change": "Password changed successfully.",
        "update_location": "Given Location has been successfully Updated.",
        "code_resend": "Unique code has been re-sent successfully.",
        "contact_us": "Your query has been submitted successfully.",
        "verify_forgot_password" : "OTP is verified successfully"
    },   
    "3000": "Ok",
}


class ErrorManager:
    """
    ErrorManager method
    """

    @staticmethod
    def get_maximum_limit_message(field_name, max_limit):
        """
        :param field_name:  field name for which blank message to be shown.
        :param max_limit: Maximum limit of field_name defined.
        :return:
        """
        return ERROR_CODE['global_error']['maximum_length'].format(field_name, max_limit)

    @staticmethod
    def get_maximum_digit_limit_message(field_name, max_limit):
        """
        :param field_name:  field name for which blank message to be shown.
        :param max_limit: Maximum limit of field_name defined.
        :return:
        """
        return ERROR_CODE['global_error']['maximum_digit'].format(field_name, max_limit)

    @staticmethod
    def get_minimum_limit_message(field_name, min_length):
        """
        :param field_name:  field name for which blank message to be shown.
        :param min_length: Minimum length of field_name defined.
        :return:
        """
        return ERROR_CODE['global_error']['minimum_character'].format(min_length, field_name)

    @staticmethod
    def get_minimum_digit_limit_message(field_name, min_length):
        """
        :param field_name:  field name for which blank message to be shown.
        :param min_length: Minimum length of field_name defined.
        :return:
        """
        return ERROR_CODE['global_error']['minimum_digit'].format(min_length, field_name)

    @staticmethod
    def get_blank_field_message(field_name):
        """
        :param field_name:  field name for which blank message to be shown.
        :return:
        """
        return ERROR_CODE['global_error']['blank_field'].format(field_name)

    @staticmethod
    def get_not_exist_message(field_name):
        """
        :param field_name:  field name for which blank message to be shown.
        :return:
        """
        return ERROR_CODE['global_error']['does_not_exist'].format(field_name)
