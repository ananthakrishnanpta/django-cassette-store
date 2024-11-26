from django.shortcuts import render
from .models import Order, OrderDetails
from cart.models import CartItem
# Create your views here.


def create_order(request):
    cart_items = CartItem.objects.filter(user = request.user)
    total_amount = sum(float(item.product.price) * item.quantity for item in cart_items)

    order = Order.objects.create(
        user = request.user,
        total_amount = total_amount,
        status = 'PENDING'
        )
    
    for item in cart_items:
        OrderDetails.objects.create(
            order=order,
            cart_item = item,
            quantity = item.quantity,
            price = item.product.price
        )
        item.delete()

    return redirect('payment:create_razorypay_order', order_id = order.id)