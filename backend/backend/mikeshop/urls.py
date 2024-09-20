from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('products/',views.products,name='products'),
   path('products/<int:prodid>/', views.product_individual, name="individual_product" )
]