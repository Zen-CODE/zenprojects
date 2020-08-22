from django.urls import path
from .api import Library

urlpatterns = [
    path('artists', Library.artists),
    path('albums/<str:artist>', Library.albums),
    path('tracks/<str:artist>/<str:album>', Library.tracks),
    path('cover/<str:artist>/<str:album>', Library.cover),
    path('random_album', Library.random_album),
    path('folder_play/<str:artist>/<str:album>', Library.folder_play),
    path('folder_enqueue/<str:artist>/<str:album>', Library.folder_enqueue),
    path('search/<str:term>', Library.search),
]
