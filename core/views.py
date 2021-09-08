import logging

from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from shop.models import Category, Purchase, Course

_logger = logging.getLogger(__name__)


class Maintenance(TemplateView):
    template_name = 'maintenance.html'


class NotFound(TemplateView):
    template_name = '404.html'


class Homepage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        context['categories'] = categories

        results = Purchase.objects.values('course_bought_id').annotate(dcount=Count('course_bought_id')).order_by(
            '-dcount')[:5]
        best_sellers = []
        for result in results:
            e = Course.objects.get(pk=result['course_bought_id'])
            best_sellers.append(e)

        context['best_seller'] = best_sellers
        return context


class AccessForbidden(TemplateView):
    template_name = 'permission_denied.html'


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('homepage')
