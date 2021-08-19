from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from users.models import UserProfile


class ProfileView(View, LoginRequiredMixin):
    profile = None

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'users/profile.html', context)