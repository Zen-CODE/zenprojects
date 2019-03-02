from django.urls import path, re_path
from . import views


app_name = "budget"

urlpatterns = [
    path('', views.index, name='index'),
    path('import_csv', views.import_csv, name='import_csv'),
    path('clear', views.clear, name='clear'),
    path('view_transactions', views.view_transactions),
    path('view_transactions/<int:imp>/', views.view_transactions,
         name='view_transactions_import'),
    path('category', views.CategoryList.as_view(),
         name='category_list'),
    path('category/<int:pk>', views.CategoryDetail.as_view(),
         name='category_detail'),
    path('category/create', views.CategoryCreate.as_view(
         success_url="/budget/category"),
         name='category_create'),
    path('category/update/<int:pk>', views.CategoryUpdate.as_view(),
         name='category_edit'),
    path('category/delete/<int:pk>', views.CategoryDelete.as_view(
         success_url="/budget/category"),
         name='category_delete'),
    path('categorization', views.CategorizationList.as_view(),
         name='categorization_list'),
    path('categorization/<int:pk>', views.CategorizationDetail.as_view(),
         name='categorization_detail'),
    path('categorization/create', views.CategorizationCreate.as_view(
         success_url="/budget/categorization"),
         name='categorization_create'),
    path('categorization/update/<int:pk>', views.CategorizationUpdate.as_view(),
         name='categorization_edit'),
    path('categorization/delete/<int:pk>', views.CategoryDelete.as_view(
         success_url="/budget/categorization"),
         name='categorization_delete'),
    # Transactions
    path('transaction', views.TransactionList.as_view(),
         name='transaction_list'),
    path('transaction/<int:pk>', views.TransactionDetail.as_view(),
         name='transaction_detail'),

]
# path(r'view_transactions/(?P<import>\w+)/$', views.view_transactions,
