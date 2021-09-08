import requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

from shop.models import Purchase, Course, Review
from shop.utils import check_if_teacher


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
        """
        Check if the user hase bought the course or if he is the teacher
        """
        check_purchase = (Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                                  buyer_id=self.request.user.id).exists())

        return check_purchase or check_if_teacher(teacher_id=self.request.user.id, course_id=self.kwargs['pk'])

    def handle_no_permission(self):
        """
        When user hasn't purchased the video show a different detail view
        """
        context = {'course': Course.objects.get(id=self.kwargs['pk'])}

        return render(request=self.request,
                      template_name='shop/course/detail_no_purchase.html',
                      context=context)


class AddCommentCheckMixin(CheckPurchaseMixin):
    def handle_no_permission(self):
        return render(request=self.request, template_name='permission_denied.html')


class ReviewChecksMixin(LoginRequiredMixin, UserPassesTestMixin):
    def __init__(self):
        self.check_purchase = False
        self.check_if_teacher = False
        self.check_already_reviewed = False

    def test_func(self):
        self.check_purchase = (Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                                       buyer_id=self.request.user.id).exists())

        self.check_if_teacher = check_if_teacher(teacher_id=self.request.user.id, course_id=self.kwargs['pk'])

        self.check_already_reviewed = (Review.objects.filter(course_id=self.kwargs['pk'],
                                                             author_id=self.request.user.id).exists())

        if (self.check_purchase and self.check_already_reviewed) or self.check_if_teacher:
            return False
        return True

    def handle_no_permission(self):
        context = {'reason': ''}

        if not self.request.user.is_authenticated:
            pass
        if not self.check_purchase:
            context['reason'] = 'You need to buy this course to review it!'
        if self.check_purchase and self.check_already_reviewed:
            context['reason'] = 'You can\'t review this course twice!'
        if self.check_if_teacher:
            context['reason'] = 'You can\'t review your own course!'

        return render(self.request, template_name='shop/review/review_permission.html', context=context)


class AlreadyBoughtMixin(LoginRequiredMixin, UserPassesTestMixin):
    def __init__(self):
        self.is_teacher = False

    def test_func(self):
        """
        Check if the user has already bought the course or if he is the teacher course
        """
        self.is_teacher = check_if_teacher(teacher_id=self.request.user.id, course_id=self.kwargs['pk'])
        if self.is_teacher:
            return False
        else:
            purchased = Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                                buyer_id=self.request.user.id).exists()
            return not purchased

    def handle_no_permission(self):
        if self.is_teacher:
            return render(request=self.request, template_name='permission_denied.html')
        else:
            return render(request=self.request,
                          template_name='shop/purchase/already_purchased.html')
