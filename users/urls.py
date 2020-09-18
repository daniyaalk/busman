from django.urls import path
from .views import UserLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='users-login'),
    # path('register/', UserRegisterView.as_view(), name='users-login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='users-logout'),
]
