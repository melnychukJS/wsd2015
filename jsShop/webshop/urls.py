from django.conf.urls import url
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from webshop.forms import RegisterForm

urlpatterns = [
	url(r'^$', 'django.contrib.auth.views.login'),
	url(r'^register/$', CreateView.as_view(
            template_name='register.html',
            form_class=RegisterForm,
            success_url='/')),
    #url(r'^logout/$', logout_page),
]