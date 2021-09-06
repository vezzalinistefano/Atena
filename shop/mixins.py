from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

from shop.models import Purchase, Course


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
        check_purchase = (Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                        buyer_id=self.request.user.id).exists())
        course = Course.objects.get(id=self.kwargs['pk'])
        check_if_teacher = course.teacher_id == self.request.user.id

        return check_purchase or check_if_teacher

    def handle_no_permission(self):
        """
        When user hasn't purchased the video show a different detail view
        """
        context = {'course': Course.objects.get(id=self.kwargs['pk'])}
        return render(request=self.request,
                      template_name='shop/course/detail_no_purchase.html',
                      context=context)
