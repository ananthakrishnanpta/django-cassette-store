from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from cart.models import CartItem
from myapp.models import Product

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="India")

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING','Pending'),('COMPLETED','Completed')])
    razorpay_order_id = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")

    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"
    
class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name="order_details", on_delete=models.CASCADE)
    order_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for order {self.order.id} - Product: {self.cart_item.product.name}"
    
    
