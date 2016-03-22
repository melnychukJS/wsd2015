from django.conf.urls import url
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from webshop.forms import RegisterForm, AddGameForm
from . import models
from webshop.models import Game

urlpatterns = [
	url(r'^$', 'django.contrib.auth.views.login'),
	url(r'^register/$', CreateView.as_view(
            template_name='register.html',
            form_class=RegisterForm,
            success_url='home')),
    url(r'^registration/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^test/$', views.add_game ),
#    url(r'^webshop/game', views.game_page(Game) )
#    url(r'^test/$', CreateView.as_view(
#    		template_name='test.html',
#    		form_class=AddGameForm,
#    		success_url='webshop/developer'
#    	))
]
