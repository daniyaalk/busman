from django.urls import path
from . import views

urlpatterns=[
    path('', views.SalesInvoiceListView.as_view(), name='sales-list'),
    path('create/', views.SalesInvoiceCreateView.as_view(), name='sales-create'),
    path('<int:pk>/edit/', views.SalesInvoiceUpdateView.as_view(), name='sales-edit'),
    path('<int:pk>/view/', views.SalesInvoiceDetailView.as_view(), name='sales-view'),
    path('<int:pk>/print/', views.SalesInvoicePrintView.as_view(), name='sales-print'),
    path('<int:pk>/delete/', views.SalesInvoiceDeleteView.as_view(), name='sales-delete'),
    path('<int:pk>/entry/add/',
         views.SalesInvoiceEntryCreateView.as_view(), name='sales-entry-add'),
    path('entry/<int:pk>/delete/',
         views.SalesInvoiceEntryDeleteView.as_view(), name='sales-entry-delete'),

]
