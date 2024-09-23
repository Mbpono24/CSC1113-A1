from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .form import *
from django.contrib.auth import login, logout
from django.views.generic import CreateView

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

def add_to_basket(request, prodid):
    user = request.user
    # is there a shopping basket for the user 
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        # create a new one
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # get the product 
    product = Product.objects.get(id=prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        # there is no basket item for that product 
        # create one 
        sbi = BasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        # a basket item already exists 
        # just add 1 to the quantity
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return redirect("/products")