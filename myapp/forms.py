from django.contrib.auth.forms import UserCreationForm
from .models import MyappUser
from django import forms


# import django UserCreationForm and inherit from it
# the class defines the user form fields that the user will have

class MyappUserCreationForm(UserCreationForm):

    # define the fields that will be required in the form
    # define the model that the form will act on in the Meta class
    # override the default help text of the fields
    # import the django form to override the fields, define the widget as form.PasswordInput
    # to hide the password being typed

    password1 = forms.CharField(label="Password",help_text="Your password must contain at least 8 characters.",
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation",
                                help_text="Enter the same password as before, for verification.",
                                widget=forms.PasswordInput())

    class Meta:
        model = MyappUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
