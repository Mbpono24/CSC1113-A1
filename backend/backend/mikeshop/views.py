from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .form import *
from django.contrib.auth import login

def index(request):
    return render(request, 'index.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products':products})

def product_individual(request, prodid):
    product = Product.objects.get(id=prodid)    
    return render(request, 'individual_products.html', {'product':product})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('index')  # Redirect to home page or any other page
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})