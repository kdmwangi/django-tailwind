import base64

from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .models import MyappUser
from .forms import MyappUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse
from requests import request as req
import os
from datetime import datetime

import environ

env = environ.Env()
environ.Env.read_env()

# read the environment variable from the env
CONSUMER_KEY = env('CONSUMER_KEY')
# second optional way to read environmental variable
# for this to work define the .env in the same folder as your settings and add it in .gitignore
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

PASS_KEY = env('PASS_KEY')
SHORT_CODE = 174379

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
        print(user.phone_number, CONSUMER_KEY, CONSUMER_SECRET)
        phone_number = str(user.phone_number).strip('+')
        print(phone_number)

        # make mpesa authorization to get the token, and make the lipa na mpesa online payment

        response = req(method='GET', url=MPESA_AUTHORIZATION_URL, params={'grant_type': 'client_credentials'},
                       auth=(CONSUMER_KEY, CONSUMER_SECRET))
        print(response.status_code)
        print(response.status_code, response.json())
        auth_token = response.json()['access_token']
        # password made up of businessshortcode+passkey+timestamp and run through base64 encoding
        print(int(datetime.now().timestamp()))
        timestamp = f'{datetime.now().year}{datetime.now().strftime("%m")}{datetime.now().day}{datetime.now().hour}' \
                    f'{datetime.now().minute}{datetime.now().second}'
        print(timestamp)
        passwd = f'{SHORT_CODE}{PASS_KEY}{timestamp}'
        print(passwd)
        p = base64.b64encode(bytes(passwd, 'utf-8'))
        password = p.decode('utf-8')

        # create a callback url webhook for mpesa
        payload = {

            "BusinessShortCode": 174379,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": 254708374149,
            "PartyB": 174379,
            "PhoneNumber": int(phone_number),
            "CallBackURL": f"https://77f5-102-140-245-169.ngrok-free.app/myapp/mpesapay/{user.id}",
            "AccountReference": "Dennis Foundation",
            "TransactionDesc": "Payment of V"
        }
        print(request.session)
        request.session['id'] = user.id

        re = req(method='POST', url=MPESA_LIPA_MPESA, headers={'Authorization': f'Bearer {auth_token}'}, json=payload)

        print(re.status_code)

    return render(request, 'myapp/transaction.html', context={})


def mpesapay(request,id):
    print("******************************")
    print(request.body)
    # req(method='POST',)
    # to decode the request sent by Mpesa Api
    response =request.body.decode(encoding='utf-8')
    print(response)
    print(id)


    return JsonResponse({}, safe=True)
