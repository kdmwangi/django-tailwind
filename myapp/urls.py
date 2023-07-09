from django.urls import path
from .views import Index,MyLoginView

# define a namespace for your app urls
app_name = 'myapp'
urlpatterns = [
    path('',Index,name='index'),
    path('login/',MyLoginView.as_view(template_name='myapp/login.html'), name='login')
]