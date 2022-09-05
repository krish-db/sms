from rest_framework.response import Response
from rest_framework import status


def response_template(data=None, status=status.HTTP_200_OK, success=True, message=[]):
    response_dict = {
        'success': success,
        'data': data,
        'errors': message
    }
    return Response(status=status, data=response_dict)


def success_response(data=None):
    return response_template(data)


def created_response(data):
    """Indicating update using post, patch, or put was successful"""
    return response_template(data, status.HTTP_201_CREATED)


def not_found_response(message, data=None):
    """Indicating that resource requested cannot be found"""
    return response_template(
        data, status.HTTP_404_NOT_FOUND, False, [message])


def general_error_response(message, data=None):
    """Indicating that request parameters or payload failed valication"""
    return response_template(
        data, status.HTTP_400_BAD_REQUEST, False, [message])

def unauthorized_error_response(message, data=None):
    return response_template(
        data, status.HTTP_401_UNAUTHORIZED, False, [message])
