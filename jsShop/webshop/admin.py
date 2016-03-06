from django.contrib import admin
from django.contrib.auth.models import User
from webshop.models import UserProfile

admin.site.register(UserProfile)
# Register your models here.
#admin.site.register(User)