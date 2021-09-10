import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from shop.models import Course, Purchase
from users.forms import UserProfileForm
from users.mixins import OwnershipMixin
from users.models import UserProfile

logger = logging.getLogger(__name__)


class UserProfileView(DetailView, LoginRequiredMixin):
    model = UserProfile
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['courses'] = Course.objects.filter(teacher_id=self.kwargs['pk'])
        context['purchases'] = Purchase.objects.filter(buyer_id=self.kwargs['pk'])
        return context


class UserProfileUpdateView(OwnershipMixin, UpdateView):
    model = UserProfile
    template_name = 'users/profile_update.html'
    form_class = UserProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})
