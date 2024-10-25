from django.urls import path
from .views import UserRegisterView, Login


urlpatterns = [
    path('signup/',UserRegisterView.as_view(), name='register'),
    path('login/', Login.as_view(),name='login')
]