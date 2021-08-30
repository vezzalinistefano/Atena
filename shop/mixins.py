from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

from shop.models import Purchase


class OwnershipMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Check if the user who is trying to do certain operations on the
    course is its creator
    """

    def test_func(self):
        return self.request.user.id == self.kwargs['teacher_id']

    def handle_no_permission(self):
        return render(request=self.request, template_name='permission_denied.html')


class CheckPurchaseMixin(UserPassesTestMixin):
    def test_func(self):
        return (Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                        buyer_id=self.request.user.id).exists())

    # TODO handle no permission by rendering to a different page similar to detail.html
    def handle_no_permission(self):
        return render(request=self.request, template_name='permission_denied.html')
