from django.urls import path
from . import views


app_name = "budget"

urlpatterns = [
    path('', views.index, name='index'),
    path('import_csv', views.import_csv, name='import_csv'),
    path('delete', views.delete, name='delete'),
    path(r'view_transactions/(?P<import>\w+)/$', views.view_transactions,
         name='view_transactions'),
]
