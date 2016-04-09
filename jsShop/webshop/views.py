from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, get_list_or_404,render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from .models import User, Game, Leaderboard, Payment
from django.template import RequestContext, loader
from webshop.forms import RegisterForm, AddGameForm, EditGameForm
from django.core.context_processors import csrf
from django.views.generic import RedirectView
from django.shortcuts import redirect
from django.db.models import Count
from datetime import datetime
from hashlib import md5
from django.contrib import messages


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			new_user = form.save()
			new_user = authenticate(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
			return HttpResponseRedirect("webshop/home.html")

		args = {}
		args.update(csrf(request))

		args['form'] = RegisterForm()

		return render_to_response('register.html', args)


def group_required(*group_names):
	"""
	Requires user membership in at least one of the groups passed in.

	Checks is_active and allows superusers to pass regardless of group
	membership.
	"""
	def in_group(u):
		return u.is_active and (u.is_superuser or bool(u.groups.filter(name__in=group_names)))
	return user_passes_test(in_group)

#function for checking if the user (u) belongs to group (name)
def in_group(u, *group):
		return bool(u.groups.filter(name__in=group))

@login_required
@group_required('Developers')
def developer(request):
	no_list=[]
	owner=request.user
	temp='foo'
	games=Game.objects.filter(author=owner)   #only his games appear in his page
	i=1
	no = Payment.objects.annotate(sales=Count('game'))

	for game in games:
		no = Payment.objects.annotate(sales=Count('game')).values

	#	temp=Game.objects.get(title=title)
		#temp1=Game.objects.filter(title=temp).
		#no = Payment.objects.filter(game=game).count
		#no_list.extend(list(no)
		no_list.append(no)
	#no=5
	#no=Game.objects.get(title=string(title))	
	return render(request, 'webshop/developer.html', {'games': games, 'no_list':no_list})


def userpage(request):
	return render(request, 'webshop/user.html')

@login_required
def user(request):
	user1=request.user
	if in_group(user1, 'Developers'):
		owner=request.user
		games=Game.objects.filter(author=owner)   #only his games appear in his page
		return render(request, 'webshop/developer.html', {'games': games})
	else:

		return render(request, 'webshop/user.html', {'user1':user1})

#@login_required
#@group_required('Developers')
#def game_page(request):
#	game=Game.objects.filter(title=request)
#	return render(request, 'webshop/game.html', {'game': games})

@login_required
def home(request):
	games = Game.objects.all()
	user1=request.user
	game_list=list ()
	payments = Payment.objects.filter(buyer=user1).values_list('game', flat=True) # quering the game the user has bought
	#payments1 = payments[0]
	for pay in payments:
		g= Game.objects.get(id=int(pay))
		game_list.append(g)

	return render_to_response('webshop/home.html', {'games':games, 'payments':payments, 'game_list': game_list})

@login_required
def game(request, id):
	temp = Game.objects.get(id=int(id))
	return render_to_response('webshop/game.html',{'temp':temp})

@login_required
def play(request, id):
	usr=request.user 
	temp = Game.objects.get(id=int(id))
	perm = Payment.objects.filter(game=temp, buyer=usr).exists()  # user can play only if he has bought the game
	if not perm: 
		messages.error(request, "You have to buy the game in order to play it! :(")  # we need to create a redirection here
	else:
		return render_to_response('webshop/play.html',{'temp':temp})

@login_required
def user_profile(request, id):
	usr=request.user
	return render_to_response('webshop/game.html',{'usr':usr})


#Adding game
@login_required
@group_required('Developers')
def add_game(request):
	form = AddGameForm(initial={'author': request.user})
	if request.method == 'POST':
		#new_game=Game(request.user)
		form = AddGameForm(request.POST, request.user)
		if form.is_valid():
			new_game=form.save(commit=False)
			new_game.author=request.user
			new_game.save()
			return HttpResponseRedirect('webshop/developer.html') #have to change !!!!
		else:
			print (form.errors)
			form = AddGameForm(initial={'author': request.user})

	return render(request, 'webshop/add-game.html',{'form': form})


#Deleting game
@login_required
@group_required('Developers')
def remove_game(request, id):
	rem=Game.objects.get(id=int(id))
	author=request.user
	if rem.author==author:
		rem.delete()
		return HttpResponse('Game deleted')

#Editing existing game
@login_required
@group_required('Developers')
def edit_game(request, id):
	game = Game.objects.get(pk=id)
	form = EditGameForm(instance = game)
	author = request.user
	if request.method == 'POST':
		form = EditGameForm(request.POST)
		if form.is_valid():
			form = EditGameForm(request.POST, instance = game)
			form.save()
			return HttpResponseRedirect('webshop/developer.html') #have to change !!!!
		else:
			game = Game.objects.get(pk = id)
			form = EditGameForm(instance=game)

	return render(request, 'webshop/edit-game.html',{'form': form})

def edit_user_profile(request):
	usr=request.userpage
	form=EditProfileForm(instance=usr)
	if request.method == 'POST':
		form = EditProfileForm(request.POST)
		if form.is_valid():
			form = EditProfileForm(request.POST, instance = usr)
			form.save()
	return render (request, 'webshop/edit_profile.html', {'form: form'})


# game sales statistics
def gameSales(request):
	if request.method == 'POST' and 'view_sales_of' in request.POST:
		g = Game.objects.filter(id=request.POST["view_sales_of"])
		g_price = Game.objects.filter(id=request.POST["view_sales_of"]).values('price')[0]
		g_title=Game.objects.filter(id=request.POST["view_sales_of"]).values('title')[0]
		title = g_title['title']
		price = g_price['price']
		sales = Payment.objects.filter(game=g).values()
		sold = len(sales)
		gain = sold * price 
		time_list = list()
		time_format = '%d-%m-%Y %H:%M:%S'
		for i in range(0, sold):
			time_list.append(sales[i]['time'].strftime(time_format))
		params = {"game_title": request.POST['view_sales_of'],'price' :price,'sales': sales, "title":title,  "sold": sold, "time_list": time_list, 'gain':gain}
		return render(request, 'webshop/gamesales.html', params)


# Buy a new game
@login_required
@group_required('Players')
def pay(request, game_id):
	if request.method == 'POST':
		game = Game.objects.get(pk = id)
		buyer = request.user
		payment = Payment(buyer, game, str(datetime.now()))
		pid = payment.id
		sid = "jsShop"
		amount = game.price
		success_url = payment.get_success_url()
		cancel_url = payment.get_cancel_url()
		error_url = payment.get_error_url()
		checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, "e9abd406499c46c34f457b17b9c97a2b")
		m = md5(checksumstr.encode("ascii"))
		checksum = m.hexdigest()
		params = {"pid": pid,'sid' :sid,'amount': amount, "success_url": success_url, "cancel_url": cancel_url, "error_url": error_url, "checksum": checksum}
		return render(request, 'webshop/game.html', params)

@login_required
@group_required('Players')
def handle_pay(request):
	if request.method == 'GET':
		pid = request.GET['pid']
        ref = request.GET['ref']
        result = request.GET['result']
        checksum = request.GET['checksum']
        sid = "jsShop"
        secret_key = "e9abd406499c46c34f457b17b9c97a2b"

        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
        m = md5(checksumstr.encode("ascii"))
		checksum2 = m.hexdigest()

		if(checksum == checksum2):
			#success
		else:
			#cancel







