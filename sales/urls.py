from django.urls import path
from . import views

urlpatterns=[
    path('', views.invoicelist, name='sales-list'),
    path('create/', views.InvoiceCreateView.as_view(), name='sales-create'),
    path('edit/<int:pk>', views.InvoiceUpdateView.as_view(), name='sales-edit'),
    path('view/<int:pk>', views.InvoiceDetailView.as_view(), name='sales-view'),
    path('add/<int:pk>', views.addentries, name='sales-add'),
]
