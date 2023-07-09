from django.contrib.auth.forms import UserCreationForm
from .models import MyappUser
# import django UserCreationForm and inherit from it
# the class defines the user form fields that the user will have

class MyappUserCreationForm(UserCreationForm):
    model = MyappUser
    # define the fields that will be required in the form
    class Meta:
        fields = ['username','email', 'phone_number','password1','password2']
