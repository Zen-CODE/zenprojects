"""
This module contains simple functions that are shared between the various apps
in this project.
"""
from rest_framework.response import Response


def get_response(results):
    """ Return the results inside of JSON api RESTful response with the CORS
    headers added.
    """
    response = Response(results)
    response["Access-Control-Allow-Origin"] = "*"
    return response
