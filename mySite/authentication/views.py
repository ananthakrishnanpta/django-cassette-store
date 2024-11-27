from django.shortcuts import render, redirect 


# Create your views here.
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    # model = User
    # fields = '__all__'
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class Login(LoginView):
    template_name = "login.html"

class PwdResetView(SuccessMessageMixin, PasswordResetView):
    template_name = "password_change_form.html"
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('homepage')
