from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .form import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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
            login(request, user) 
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
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


@login_required
def view_basket(request):
    if not request.user.is_authenticated:
        return redirect('/login') 
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return render(request, 'view_basket.html', {'empty': True})

    basket_items = BasketItem.objects.filter(basket_id=basket)
    total_price = sum(item.item_price() for item in basket_items)

    context = {
        'basket': basket,
        'basket_items': basket_items,
        'total_price': total_price
    }
    return render(request, 'view_basket.html', context)


@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        basket_item = get_object_or_404(BasketItem, id=item_id)
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity > 0:
            basket_item.quantity = new_quantity
            basket_item.save()
        return redirect('view_basket')
    

@login_required
def remove_from_basket(request, item_id):
    if request.method == 'POST':
        basket_item = get_object_or_404(BasketItem, id=item_id)
        basket_item.delete()
        return redirect('view_basket')
    

@login_required
def checkout(request):
    basket = Basket.objects.filter(user_id=request.user, is_active=True).first()

    if not basket:
        return redirect('view_basket')

    total_price = sum(item.item_price() for item in basket.basketitem_set.all())

    order = Order.objects.create(
        user_id=request.user,
        basket_id=basket,    
        total_price=total_price
    )
    basket.is_active = False
    basket.save()

    return redirect('order_confirmation', order_id=order.id)


@login_required
def view_orders(request):
    orders = Order.objects.filter(user_id=request.user).order_by('-date_ordered')
    return render(request, 'view_orders.html', {'orders': orders})


@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user_id=request.user)
    return render(request, 'order_confirmation.html', {'order': order})