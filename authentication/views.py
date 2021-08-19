from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authentication.forms import RegisterForm
from users.models import UserProfile


class UserCreate(CreateView):
    model = UserProfile
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('homepage')
    form_class = RegisterForm


class UserLogin(LoginView):
    model = UserProfile
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('homepage')


class UserLogout(LogoutView):
    template_name = 'authentication/logged_out.html'
