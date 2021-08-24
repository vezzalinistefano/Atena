import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from shop.models import Course
from users.models import UserProfile

logger = logging.getLogger(__name__)


class UserProfileView(DetailView, LoginRequiredMixin):
    template_name = 'users/profile.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        print(self.kwargs)
        context['courses'] = Course.objects.filter(teacher_id=self.kwargs['pk'])
        return context
