from django.http import HttpResponse
from django.shortcuts import render
from .models import *

def index(request):
    return render(request, 'index.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products':products})


def product_individual(request, prodid):
    product = Product.objects.get(id=prodid)    
    return render(request, 'individual_products.html', {'product':product})