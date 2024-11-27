from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from cart.models import CartItem
from .models import Order, OrderDetails

@login_required
def create_order(request):
    """Create an order from the user's cart items."""
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    
    if not cart_items.exists():
        # Redirect to an empty cart page if no items in the cart
        return render(request, 'cart.html')

    # Calculate the total amount of the cart
    total_amount = sum(item.quantity * item.product.price for item in cart_items)

    # Create an order record
    order = Order.objects.create(
        user=user,
        total_amount=total_amount,
        order_date=now(),
        status='PENDING'
    )

    # Create order detail records for each cart item
    for item in cart_items:
        OrderDetails.objects.create(
            order=order,
            cart_item=item,
            quantity=item.quantity,
            price=item.product.price * item.quantity
        )
    
    # Clear the cart after creating the order
    cart_items.delete()

    # Redirect to the Razorpay payment flow
    return redirect('payment:create_razorpay_order', order_id=order.id)


@login_required
def order_history(request):
    """Display a list of all orders for the logged-in user."""
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-order_date')
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Display details of a specific order."""
    user = request.user
    order = get_object_or_404(Order, id=order_id, user=user)
    return render(request, 'order_detail.html', {'order': order})
