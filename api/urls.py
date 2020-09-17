from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('categories/', views.categoryAutoComplete, name="api-categories"),
    path('names/', views.nameAutoComplete, name="api-names"),
    path('brands/', views.brandAutoComplete, name="api-brands"),
]
