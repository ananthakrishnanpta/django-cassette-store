from django.shortcuts import render, redirect 
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm 
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import ProfileForm

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
class Login(LoginView):
    template_name = "login.html"
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'



@login_required
def profile_view(request):
    # Try to get the user's profile, or create one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the profile page after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})