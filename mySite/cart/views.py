from django.shortcuts import render, redirect
from .models import Product, CartItem
# importing login_required decorator to control access to views
from django.contrib.auth.decorators import login_required

# implementing AJAX to update cart item quantity without refresh
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def viewCart(request):
    template = 'cart.html'
    cart_items = CartItem.objects.filter(user = request.user) 
    # select * from CartItem where user = authenticated_user_who_sent_request
    total_price = sum(float(item.product.price) * item.quantity for item in cart_items)

    context = {
        'cart_items' : cart_items,
        'total_price' : total_price
    }
    return render(request, template, context)

def addToCart(request, product_id):
    this_product = Product.objects.get(id = product_id)
    cart_item, created = CartItem.objects.get_or_create(product=this_product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    # insert into CartItem(product, user) values(this_product, request.user) on duplicate key update quantity = quantity + 1
    return redirect('cart:view_cart')

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id = cart_item_id) 
    # filter and get the particular cart item object filtered pk
    # this pk is obtained from the particular path of each items' link on remove button
    cart_item.delete()
    return redirect('cart:view_cart')


@login_required
def add_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    overall_total = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
    return JsonResponse({'quantity': cart_item.quantity, 'total_price': cart_item.get_total_price(), 'overall_total': overall_total})

@login_required
def remove_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        overall_total = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
        return JsonResponse({'quantity': cart_item.quantity, 'total_price': cart_item.get_total_price(), 'overall_total': overall_total})
    else:
        cart_item.delete()
        overall_total = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
        return JsonResponse({'quantity': 0, 'total_price': 0, 'overall_total': overall_total})