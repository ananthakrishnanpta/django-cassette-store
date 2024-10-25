from django.shortcuts import render, redirect 


# Create your views here.
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    # model = User
    # fields = '__all__'
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class Login(LoginView):
    template_name = "login.html"
