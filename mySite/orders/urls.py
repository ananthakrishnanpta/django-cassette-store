from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # Route to create a new order
    path('create/', views.create_order, name='create_order'),
    
    # Route to display the user's order history
    path('order_history/', views.order_history, name='order_history'),
    
    # Route to view details of a specific order
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
