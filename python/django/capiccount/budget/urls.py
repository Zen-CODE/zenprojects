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
]
# path(r'view_transactions/(?P<import>\w+)/$', views.view_transactions,
