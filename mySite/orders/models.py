from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from cart.models import CartItem

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING','Pending'),('COMPLETED','Completed')])
    razorpay_order_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"
    
class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name="order_details", on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for order {self.order.id} - Product: {self.cart_item.product.name}"
    
    
