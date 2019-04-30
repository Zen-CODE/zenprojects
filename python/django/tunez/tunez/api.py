"""
This module houses the main view functions for the media player controller
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def artists(request):
    """
    Return a list of artists in our library.
    """
    return Response({"artists": ["Ace of Base", "BT"]})



