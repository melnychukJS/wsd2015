from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms 
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, get_list_or_404,render_to_response
from django.contrib.auth.decorators import login_required
from django.db import models
<<<<<<< HEAD
=======
from .models import User, Game, Leaderboard, Payment
>>>>>>> 55d43a36ca97570524db6232cdf748253cd56a48
from django.template import RequestContext, loader
from webshop.forms import RegisterForm

def starting_instructions(request):
	return render(request, "webshop/instructions.html", {})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			new_user = form.save()
			new_user = authenticate(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])            
			return HttpResponseRedirect("registration/login.html")
	
		args = {}
		args.update(csrf(request))	

		args['form'] = RegisterForm()

		return render_to_response('register.html', args)


	#else:
	#	form = RegisterForm()
	#return render(request, "registration/login.html", {
	#	'form': form,
	#})    

def about(request):
	return HttpResponse("about page")



def available_products(request):
    available = get_list_or_404(Product,quantity__gt=0)
    return render_to_response('webshop/product_list.html', {'products':available})

def developer(request):
    return render_to_response('webshop/developer.html')

def home(request):
    return render_to_response('webshop/home.html')

def user(request):
    return render_to_response('webshop/user.html')
