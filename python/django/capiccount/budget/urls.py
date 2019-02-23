from django.urls import path, re_path
from . import views


app_name = "budget"

urlpatterns = [
    path('', views.index, name='index'),
    path('import_csv', views.import_csv, name='import_csv'),
    path('delete', views.delete, name='delete'),
    path('view_transactions', views.view_transactions),
    path('view_transactions/<int:imp>/', views.view_transactions,
    # path(r'view_transactions/(?P<import>\w+)/$', views.view_transactions,
         name='view_transactions_import'),
]
