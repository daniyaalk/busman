from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.dash, name='org-dash'),
    path('none/', views.noOrgView, name='org-none'),
    path('create/', views.OrganizationCreateView.as_view(), name='org-create'),
]
