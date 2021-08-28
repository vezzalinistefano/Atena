from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy


class OwnershipMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        return render(request=self.request, template_name='permission_denied.html')