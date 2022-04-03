from django.urls import path
from zenplayer import views
from zenplayer.views import UIView

urlpatterns = [
    path('', views.index, name='index'),
    path('ui/', UIView.as_view(), name='ui'),
]
