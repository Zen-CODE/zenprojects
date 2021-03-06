"""tunez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .api import Player

urlpatterns = [
    path('previous', Player.previous),
    path('stop', Player.stop),
    path('play_pause', Player.play_pause),
    path('next', Player.next),
    path('volume_up', Player.volume_up),
    path('volume_down', Player.volume_down),
    path('state', Player.state),
    path('cover', Player.cover),
    path('volume_set/<str:volume>', Player.volume_set),
    path('message_add/<str:msg_type>/<str:msg>', Player.message_add),
]
