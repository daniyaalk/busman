from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name='products-list'),
    # path("add/", views.ProductCreateView.as_view(), name='products-create'),
    path("add/", views.ProductCreateView.as_view(), name='products-add'),
    path("edit/<int:pk>", views.ProductUpdateView.as_view(), name='products-edit'),
    path("delete/<int:pk>", views.ProductDeleteView.as_view(), name='products-delete'),
]
