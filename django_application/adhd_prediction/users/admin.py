from django.contrib import admin
from .models import Profile
# Register your models here
#why should the model  be registered in the admin.py file

admin.site.register(Profile)
