from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

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

def register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('org-dash')

    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})