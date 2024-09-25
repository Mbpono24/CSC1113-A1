from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('products/',views.products,name='products'),
   path('register/', views.register, name='register'),
   path('products/<int:prodid>/', views.product_individual, name="individual_product" ),
   path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('addbasket/<int:prodid>/', views.add_to_basket, name="add_basket"),
   path('view-basket/', views.view_basket, name='view_basket'),
   path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
   path('remove-from-basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
   path('checkout/', views.checkout, name='checkout'),
   path('orders/', views.view_orders, name='view_orders'),
   path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation')
]