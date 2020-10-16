from django.urls import path
from .views import UserLoginView, register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='users-login'),
    path('register/', register, name='users-register'),
    path('logout/', LogoutView.as_view(next_page="/"), name='users-logout'),
]
