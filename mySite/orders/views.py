from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from cart.models import CartItem
from .models import Order, OrderDetails, Address
from .forms import AddressForm


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
            order_item=item.product,
            quantity=item.quantity,
            price=item.product.price * item.quantity
        )
    
    # Clear the cart after creating the order
    cart_items.delete()

    # Redirect to the Razorpay payment flow
    return redirect('payment:create_razorpay_order', order_id=order.id)


def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).prefetch_related('order_details').order_by('-order_date')

    context =  {
        'orders': orders
        }
    return render(request, 'order_history.html', context)


@login_required
def order_detail(request, order_id):
    """Display details of a specific order."""
    user = request.user
    order = get_object_or_404(Order, id=order_id, user=user)
    return render(request, 'order_detail.html', {'order': order})



@login_required
def add_address(request):
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')  # Redirect to profile or a page listing addresses
    return render(request, 'add_address.html', {'form': form})


@login_required
def select_address_for_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    addresses = request.user.addresses.all()

    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = get_object_or_404(Address, id=address_id, user=request.user)
        order.address = address
        order.save()
        return redirect('order_history')  # Redirect to order history or order details page

    return render(request, 'select_address.html', {'order': order, 'addresses': addresses})


