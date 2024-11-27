from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')],
        default='PENDING'
    )

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
