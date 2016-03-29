from django.contrib import admin
from django.contrib.auth.models import User
from webshop.models import UserProfile, Game, Payment

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Payment)
# Register your models here.
#admin.site.register(User)