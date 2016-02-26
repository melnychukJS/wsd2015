from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404,render_to_response
from django.db import models
from .models import Product
from django.template import RequestContext, loader

def starting_instructions(request):
    return render(request, "webshop/instructions.html", {})

def about(request):
    return HttpResponse("about page")

def productview(request, product_id):
    obj = get_object_or_404(Product,pk=product_id)
    return render(request, 'webshop/product_view.html', {'product':obj})

def available_products(request):
    available = get_list_or_404(Product,quantity__gt=0)
    return render_to_response('webshop/product_list.html', {'products':available})
