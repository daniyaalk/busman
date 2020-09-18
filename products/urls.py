from django.urls import path
from . import views

urlpatterns = [
    path("", views.productlist, name='products-list'),
    path("add/", views.ProductCreateView.as_view(), name='products-add'),
    path("edit/<int:pk>", views.ProductUpdateView.as_view(), name='products-edit'),
    path("delete/<int:pk>", views.ProductDeleteView.as_view(), name='products-delete'),
]
