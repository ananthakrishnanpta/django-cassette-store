import razorpay
from django.conf import settings

from django.shortcuts import render, redirect

from django.http import JsonResponse
from .models import Payment
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(request, order_id):
    # This function creates a razorpay order to initiate checkout process
    order = Order.objects.get(id=order_id)
    razorpay_order_data = {
        "amount" : int(order.total_amount * 100),
        "currency": "INR",
        "receipt": f"order_rcpt_{order_id}",
        "payment_capture" : 1
    }

    razorpay_order = client.order.create(data = razorpay_order_data)
    order.razorpay_order_id = razorpay_order['id']
    order.save()

    context = {
        "payment/checkout.html", {
            "razorpay_order": razorpay_order,
            "order" : order,
            "key_id": settings.RAZORPAY_KEY_ID
        }
    }
    return render(request, context)

# @csrf_exempt
# def payment_success(request):
#     razorpay_order_id = request.POST.get('razor_order_id')
#     razorpay_payment_id = request.POST.get('razorpay_payment_id')
#     razorpay_signature = request.POST.get('razorypay_signature')


