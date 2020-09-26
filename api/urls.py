from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),

    path('categories/', views.CategoryAutocomplete.as_view(), name="api-categories"),
    path('names/', views.NameAutocomplete.as_view(), name="api-names"),
    path('brands/', views.BrandAutocomplete.as_view(), name="api-brands"),
]
