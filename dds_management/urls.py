from django.urls import path
from . import views

app_name = 'dds_management'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('transaction/add/', views.TransactionCreateUpdateView.as_view(), name='transaction_add'),
    path('transaction/<int:pk>/edit/', views.TransactionCreateUpdateView.as_view(), name='transaction_edit'),
    path('transaction/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('references/', views.ReferenceManagementView.as_view(), name='reference_management'),
    path('references/<str:model_name>/add/', views.ReferenceCreateView.as_view(), name='reference_add'),
    path('references/<str:model_name>/<int:pk>/delete/', views.ReferenceDeleteView.as_view(), name='reference_delete'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
]