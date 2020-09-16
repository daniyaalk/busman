from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

# Create your views here.
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Login'
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('org-dash')
        else:
            return super().get(request, *args, **kwargs)