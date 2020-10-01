from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchaselist, name='purchase-list'),
    path('create/', views.PurchaseCreateView.as_view(), name='purchase-create'),
    path('<int:pk>/view/', views.PurchaseDetailView.as_view(), name='purchase-view'),
    path('<int:pk>/edit/', views.PurchaseUpdateView.as_view(), name='purchase-edit'),
    path('<int:pk>/delete/', views.PurchaseDeleteView.as_view(), name='purchase-delete'),
    path('<int:pk>/entry/add/', views.PurchaseEntryCreateView.as_view(),
         name='purchase-entry-add'),
    path('entry/<int:pk>/delete/', views.PurchaseEntryDeleteView.as_view(),
         name='purchase-entry-delete'),
]
