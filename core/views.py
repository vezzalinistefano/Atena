import logging

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm

_logger = logging.getLogger(__name__)


class Maintenance(TemplateView):
    template_name = 'maintenance.html'


class NotFound(TemplateView):
    template_name = '404.html'


class Homepage(TemplateView):
    template_name = 'home.html'


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('homepage')
