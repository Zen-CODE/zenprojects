from django.urls import path
from zenplayer import views

urlpatterns = [
    path('', views.index, name='index'),
]
