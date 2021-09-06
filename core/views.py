import logging

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from shop.models import Course

_logger = logging.getLogger(__name__)


class Maintenance(TemplateView):
    template_name = 'maintenance.html'


class NotFound(TemplateView):
    template_name = '404.html'


class Homepage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        categories = [c for c in Course.CATEGORY_CHOICES]
        print(categories)
        context['categories'] = categories
        return context


class AccessForbidden(TemplateView):
    template_name = 'permission_denied.html'


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('homepage')
