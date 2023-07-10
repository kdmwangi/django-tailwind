from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .models import MyappUser
from .forms import MyappUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from requests import request as req
import os

N = os.environ.get('CONSUMER_KEY')

MPESA_AUTHORIZATION_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
MPESA_LIPA_MPESA = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

# Create your views here.
def Index(request):
    return render(request, 'myapp/index.html', context={})


# create a view to handle login, inherit the LoginView from django.contrib.auth.views

class MyLoginView(LoginView):
    model = MyappUser


# create a user registration form and view instance
def register_view(request):
    return render(request, 'myapp/register.html', context={})


def registration(request):
    form = MyappUserCreationForm()
    if request.method == 'POST':
        form = MyappUserCreationForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return render(request, '', context={})
    else:
        if request.user.is_authenticated:
            # when the user tries to access the registration page they are already logged in
            # use the HttpResponseRedirect() so that the url on the user browser maintains its state
            # pass the reverse method as a parameter with the view name
            return HttpResponseRedirect(reverse('myapp:donation'))
            # return render(request,'myapp/transaction.html',context={})

    return render(request, 'myapp/register.html', context={'form': form})


# view function for donations after login, give it a @login_required decorator function

@login_required
def donation(request):
    if request.method == 'POST':
        print(request.method)
        user = MyappUser.objects.filter(username=request.user.username)[0]
        print(user.phone_number, N)
        # make mpesa authorization to get the token, and make th lipa na mpesa online payment

        response = req(method='POST', url=MPESA_AUTHORIZATION_URL, auth=())

    return render(request, 'myapp/transaction.html', context={})
