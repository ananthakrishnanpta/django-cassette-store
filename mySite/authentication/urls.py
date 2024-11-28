from django.urls import path
from .views import UserRegisterView, Login, CustomPasswordResetCompleteView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetView
from .views import profile_view


urlpatterns = [
    path('signup/',UserRegisterView.as_view(), name='register'),
    path('login/', Login.as_view(),name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', profile_view, name='profile'),
]