from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('create_order/<int:order_id>/', views.create_razorpay_order, name='create_razorpay_order'),
    path('success/', views.payment_success, name='payment_success'),
]
    