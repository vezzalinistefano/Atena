from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from forum.models import Review
from shop.models import Purchase
from shop.utils import check_if_teacher


class AddCommentCheckMixin(UserPassesTestMixin):
    def __init__(self):
        self.check_purchase = False
        self.check_if_teacher = False

    def test_func(self):
        self.check_purchase = (Purchase.objects.filter(course_bought_id=self.kwargs['course_pk'],
                                                       buyer_id=self.request.user.id).exists())
        self.check_if_teacher = check_if_teacher(teacher_id=self.request.user.id, course_id=self.kwargs['course_pk'])
        if self.check_purchase or self.check_if_teacher:
            return True
        return False

    def handle_no_permission(self):
        context = {'reason': ''}

        if not self.request.user.is_authenticated:
            pass
        elif not self.check_purchase:
            context['reason'] = 'You need to buy this course to comment it!'

        return render(self.request, template_name='forum/review/review_permission.html', context=context)


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

        return render(self.request, template_name='forum/review/review_permission.html', context=context)


class ReviewUpdateMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        """Check if the review has been created by the user who wants to do the update"""
        review = Review.objects.get(id=self.kwargs['pk'])

        return self.request.user.id == review.author_id

    def handle_no_permission(self):
        if self.check_purchase and (not self.check_already_reviewed):
            return render(reverse_lazy('forum:add-review', kwargs={'pk': self.kwargs['pk']}))

        return render(request=self.request, template_name='permission_denied.html')
