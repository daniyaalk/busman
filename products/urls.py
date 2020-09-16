from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name='products-list'),
    # path("add/", views.ProductCreateView.as_view(), name='products-create'),
    path("add/", views.addProducts, name='products-add'),
]
