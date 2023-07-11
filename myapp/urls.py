from django.urls import path
from .views import Index, MyLoginView, registration, donation, mpesapay
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt

# for urls dealing with json data you need to exempt csrf_token
# define a namespace for your app urls for django.contrib.auth.views to work you need to provide the LOGIN_URL
# variable in settings, this will redirect the user to the login page automatically redirect_authenticated_user
# parameter in the LoginView to redirect user who are logged in already
app_name = 'myapp'
urlpatterns = [
    path('', Index, name='index'),
    path('login/', MyLoginView.as_view(template_name='myapp/login.html', redirect_authenticated_user=True),
         name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', LogoutView.as_view(next_page='myapp:index'), name='logout'),
    path('donate/', donation, name='donation'),
    path('mpesapay/<int:id>',csrf_exempt(mpesapay),name='mpesapay')
]
