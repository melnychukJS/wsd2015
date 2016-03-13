from django.contrib import admin
from django.contrib.auth.models import User
from webshop.models import UserProfile, Game

admin.site.register(UserProfile)
admin.site.register(Game)
# Register your models here.
#admin.site.register(User)