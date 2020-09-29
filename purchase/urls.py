from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchaselist, name='purchase-list'),
    path('create/', views.PurchaseInvoiceCreateView.as_view(),
         name='purchase-create'),
    path('<int:pk>/view/', views.PurchaseInvoiceDetailView.as_view(),
         name='purchase-view'),
    path('<int:pk>/edit/', views.PurchaseInvoiceUpdateView.as_view(),
         name='purchase-edit'),
    path('<int:pk>/delete/', views.PurchaseInvoiceDeleteView.as_view(),
         name='purchase-delete'),
    path('<int:pk>/entry/add/', views.PurchaseInvoiceEntryCreateView.as_view(),
         name='purchase-entry-add'),
    path('entry/<int:pk>/delete/', views.PurchaseInvoiceEntryDeleteView.as_view(),
         name='purchase-entry-delete'),
]
