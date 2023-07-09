from django.contrib import admin
from .models import MyappUser

# make your model accessible in django admin
# Register your models here.
admin.site.register(MyappUser)
