from django.contrib import admin
from django.contrib.auth.models import User
from webshop.models import UserProfile, Game, Payment, Save

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Payment)
admin.site.register(Save)
# Register your models here.
#admin.site.register(User)
