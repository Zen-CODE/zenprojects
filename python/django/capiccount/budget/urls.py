from django.urls import path
from .views import category, categorization, transaction, views


app_name = "budget"

urlpatterns = [
    path('', views.index, name='index'),
    path('clear', views.clear, name='clear'),

    # Import
    path('import_csv', views.import_csv, name='import_csv'),
    path('import_result/<int:success>', views.import_result,
         name='import_result'),

    # Categories
    path('category', category.CategoryList.as_view(),
         name='category_list'),
    path('category/<int:pk>', category.CategoryDetail.as_view(),
         name='category_detail'),
    path('category/create', category.CategoryCreate.as_view(
         success_url="/budget/category"),
         name='category_create'),
    path('category/update/<int:pk>', category.CategoryUpdate.as_view(),
         name='category_edit'),
    path('category/delete/<int:pk>', category.CategoryDelete.as_view(
         success_url="/budget/category"),
         name='category_delete'),

    # Categorizations
    path('categorization', categorization.CategorizationList.as_view(),
         name='categorization_list'),
    path('categorization/<int:pk>', categorization.CategorizationDetail.as_view(),
         name='categorization_detail'),
    path('categorization/create', categorization.CategorizationCreate.as_view(
         success_url="/budget/categorization"),
         name='categorization_create'),
    path('categorization/update/<int:pk>', categorization.CategorizationUpdate.as_view(),
         name='categorization_edit'),
    path('categorization/delete/<int:pk>', categorization.CategorizationDelete.as_view(
         success_url="/budget/categorization"),
         name='categorization_delete'),
    path('cat_assign/<int:pk>', categorization.cat_assign, name='cat_assign'),

    # Transactions
    path('transaction', transaction.TransactionList.as_view(),
         name='transaction_list'),
    path('transaction/<int:pk>', transaction.TransactionDetail.as_view(),
         name='transaction_detail'),

    # Category Analysis
    path('category_analysis', views.category_analysis,
         name='category_analysis'),

]
# path(r'view_transactions/(?P<import>\w+)/$', views.view_transactions,
