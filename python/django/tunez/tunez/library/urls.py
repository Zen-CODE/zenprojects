from django.urls import path
from .api import Library

urlpatterns = [
    path('artists', Library.artists),
    path('albums/<str:artist>', Library.albums),
    path('tracks/<str:artist>/<str:album>', Library.tracks),
    path('cover/<str:artist>/<str:album>', Library.cover),
]
