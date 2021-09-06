from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

from shop.models import Purchase, Course, Review


class OwnershipMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Check if the user who is trying to do certain operations on the
    course is its creator
    """

    def test_func(self):
        return self.request.user.id == self.kwargs['teacher_id']

    def handle_no_permission(self):
        return render(request=self.request, template_name='permission_denied.html')


class CheckPurchaseMixin(LoginRequiredMixin, UserPassesTestMixin):
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


class ReviewChecksMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        self.check_purchase = (Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                                       buyer_id=self.request.user.id).exists())

        course = Course.objects.get(id=self.kwargs['pk'])
        self.check_if_teacher = course.teacher_id == self.request.user.id

        self.check_already_reviewed = (Review.objects.filter(course_id=self.kwargs['pk'],
                                                             author_id=self.request.user.id).exists())

        if not ((self.check_purchase and self.check_already_reviewed) or self.check_if_teacher):
            return False
        return True

    def handle_no_permission(self):
        context = {'reason': ''}

        if not self.request.user.is_authenticated:
            pass
        elif not self.check_purchase:
            context['reason'] = 'You need to buy this course to review it!'
        elif self.check_purchase and self.check_already_reviewed:
            context['reason'] = 'You can\'t review this course twice!'
        elif self.check_if_teacher:
            context['reason'] = 'You can\'t review your own course!'

        return render(self.request, template_name='shop/review/review_permission.html', context=context)


class AlreadyBoughtMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (not Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                            buyer_id=self.request.user.id).exists())

    def handle_no_permission(self):
        return render(request=self.request,
                      template_name='shop/purchase/already_purchased.html')
