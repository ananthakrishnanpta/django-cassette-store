import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Payment
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_razorpay_order(request, order_id):
    """Create a Razorpay order and initiate the checkout process."""
    order = Order.objects.get(id=order_id)
    
    # Create Razorpay order
    razorpay_order_data = {
        "amount": int(order.total_amount * 100),  # Convert to paisa
        "currency": "INR",
        "receipt": f"order_rcpt_{order.id}",
        "payment_capture": 1  # Auto capture payments
    }
    razorpay_order = client.order.create(data=razorpay_order_data)
    
    # Save the Razorpay order ID to the Order
    order.razorpay_order_id = razorpay_order['id']
    order.save()

    context = {
        "razorpay_order": razorpay_order,
        "order": order,
        "key_id": settings.RAZORPAY_KEY_ID
    }

    return render(request, "checkout.html", context )

@csrf_exempt
def payment_success(request):
    """Handle the Razorpay payment success callback."""
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    try:
        # Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
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
            status="COMPLETED"
        )

        return render(request, "success.html", {"order": order})

    except razorpay.errors.SignatureVerificationError:
        return render(request, "failure.html", {"error": "Payment verification failed!"})
