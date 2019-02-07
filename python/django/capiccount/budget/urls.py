from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('import', views.import_csv, name='import'),
    path('view_transactions', views.view_transactions,
         name='view_transactions'),
]
