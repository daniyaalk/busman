from django.urls import path
from . import views

urlpatterns=[
    path('', views.invoicelist, name='sales-list'),
    path('create/', views.InvoiceCreateView.as_view(), name='sales-create'),
    path('edit/<int:pk>', views.InvoiceUpdateView.as_view(), name='sales-edit'),
]
