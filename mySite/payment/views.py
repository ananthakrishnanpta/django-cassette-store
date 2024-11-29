import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from orders.models import Order, Address

from orders.forms import AddressForm

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def create_razorpay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        # Handling Address Selection
        if "address_id" in request.POST:
            selected_address = get_object_or_404(Address, id=request.POST["address_id"], user=request.user)
            order.address = selected_address
            order.save()
        
        # Handling Add Address
        elif "add_address" in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                new_address = address_form.save(commit=False)
                new_address.user = request.user
                new_address.save()
                order.address = new_address
                order.save()
                return redirect('payment:create_razorpay_order', order_id=order.id)  # Redirect after adding address
            else:
                return render(request, "checkout.html", {
                    "order": order,
                    "addresses": addresses,
                    "address_form": address_form,
                    "error": "Invalid address data."
                })

        # Razorpay Order Creation
        razorpay_order_data = {
            "amount": int(order.total_amount * 100),  # Convert to paisa
            "currency": "INR",
            "receipt": f"order_rcpt_{order.id}",
            "payment_capture": 1
        }
        razorpay_order = client.order.create(data=razorpay_order_data)
        order.razorpay_order_id = razorpay_order["id"]
        order.save()
        print("this>>>",order.razorpay_order_id)

        context = {
            "razorpay_order": razorpay_order,
            "order": order,
            "key_id": settings.RAZORPAY_KEY_ID,
            "addresses": addresses,
            "address_form": AddressForm(),  # If no address, show the form
        }

        return render(request, "checkout.html", context)

    return render(request, "checkout.html", {
        "order": order,
        "addresses": addresses,
        "address_form": AddressForm(),
    })


@csrf_exempt
def payment_success(request):
    """Handle the Razorpay payment success callback."""
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    try:
        # Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        })

        # Fetch the order associated with the Razorpay order ID
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        order.status = "COMPLETED"
        order.save()

        # Create Payment record
        Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            status="COMPLETED",
        )

        return render(request, "success.html", {"order": order})

    except razorpay.errors.SignatureVerificationError:
        return render(request, "failure.html", {"error": "Payment verification failed!"})
