import base64
import json

from django.shortcuts import render
from django.contrib.auth import authenticate,login
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
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request,user)
            return render(request, 'myapp/index.html', context={})
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
        # when the session middleware is activated in the settings middleware
        # every view function will have a session object passed through the request
        # you can set the expiry of the user session by passing the variable in seconds

        request.session.set_expiry(300)
        request.session.get_expire_at_browser_close()
        # print(request.session)
        print(request.method)
        user = MyappUser.objects.filter(username=request.user.username)[0]
        print(user.phone_number, CONSUMER_KEY, CONSUMER_SECRET)
        phone_number = str(user.phone_number).strip('+')
        print(phone_number)

        # make mpesa authorization to get the token, and make the lipa na mpesa online payment
        # daraja api has switched to bearer_token for you to access the auth_token from you need to encode the
        # consumer key and secret key using b64encode
        secret_key = f'{CONSUMER_KEY}:{CONSUMER_SECRET}'
        skey = secret_key.encode('ascii')
        b_token = base64.b64encode(skey).decode('ascii')
        print(b_token)

        response = req(method='GET', url=MPESA_AUTHORIZATION_URL,
                       headers={'Authorization': f"Basic {b_token}"})
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
            "CallBackURL": f"https://26e1-197-231-183-178.ngrok-free.app/myapp/mpesapay/{user.id}",
            "AccountReference": "Dennis Foundation",
            "TransactionDesc": "Payment of V"
        }
        print(request.session)
        request.session['id'] = user.id

        re = req(method='POST', url=MPESA_LIPA_MPESA, headers={'Authorization': f'Bearer {auth_token}'}, json=payload)

        print(re.status_code)

    return render(request, 'myapp/transaction.html', context={})


def mpesapay(request, id):
    # to decode the request sent by Mpesa Api
    response = json.loads(request.body.decode(encoding='utf-8'))
    print(response)
    if 'CallbackMetadata' in response:
        print(response['Body'])

    receipt = response['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    usr = MyappUser.objects.get(id=int(id))
    usr.mympesadonations_set.create(mpesa_code=receipt, mpesa_request_body=response)

    return JsonResponse({}, safe=True)
