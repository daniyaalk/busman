from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, template_name="home/home.html", context=context)