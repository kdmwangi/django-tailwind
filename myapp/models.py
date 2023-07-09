from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
# use the AbstractUser to create a user model similar to django admin
# when you abstract from the user model you can add additional fields import the phonenumber and construct
# when abstracting the User model you need to specify the AUTH_USER_MODEL='path to your custom user class' in settings
# as your custom class
class MyappUser(AbstractUser):
    phone_number = PhoneNumberField()
    email = models.EmailField()
