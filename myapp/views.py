from django.shortcuts import render
from django.contrib.auth.views import  LoginView
from .models import MyappUser

# Create your views here.
def Index(request):

    return render(request, 'myapp/index.html', context={})
# create a view to handle login, inherit the LoginView from django.contrib.auth.views

class MyLoginView(LoginView):
    model = MyappUser

