from django.urls import path
from . import views 

app_name = 'cart'

urlpatterns = [
    path('cart/', views.viewCart, name='view_cart'),
    path('add/<int:product_id>', views.addToCart, name='add_to_cart'),
    path('remove/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('cart/add/<int:cart_item_id>/', views.add_quantity, name='add_quantity'),
    path('cart/remove/<int:cart_item_id>/', views.remove_quantity, name='remove_quantity'),
]