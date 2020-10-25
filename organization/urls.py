from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.dash, name='org-dash'),
    path('none/', views.noOrgView, name='org-none'),
    path('create/', views.OrganizationCreateView.as_view(), name='org-create'),
    path('join/', views.OrganizationRequestFormView.as_view(), name='org-join'),
    path('settings/', views.OrganizationUpdateView.as_view(), name='org-settings'),
    path('requests/', views.OrganizationRequestListView.as_view(), name='org-requests'),
    path('requests/action', views.request_action, name='org-requests-action'),

]
