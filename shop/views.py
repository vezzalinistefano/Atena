import logging
import constants

import vimeo
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.db.utils import OperationalError
from filters import CourseFilter
from shop.forms import PurchaseForm, AddCommentForm, CourseUploadForm, CourseUpdateForm, AddReviewForm, \
    AddReplyForm
from shop.mixins import OwnershipMixin, CheckPurchaseMixin, AlreadyBoughtMixin, ReviewChecksMixin, AddCommentCheckMixin
from shop.models import Course, Purchase, Comment, Review, Category, CommentReply

logger = logging.getLogger(__name__)


class CreateViewVimeo(UserPassesTestMixin, LoginRequiredMixin, View):
    form_class = CourseUploadForm
    template_name = 'shop/course/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        data = self.form_class(request.POST, request.FILES)
        post_data = request.POST
        try:
            if data.is_valid():
                client = vimeo.VimeoClient(
                    token=f'{constants.ACCESS_TOKEN}',
                    key=f'{constants.CLIENT_ID}',
                    secret=f'{constants.CLIENT_SECRET}'
                )
                uri = client.upload(request.FILES['video'].temporary_file_path(),
                                    data={
                                        'name': f'{post_data["title"]}',
                                        'description': f'{post_data["description"]}'
                                    })
                Course.objects.create(
                    title=post_data['title'],
                    teacher=request.user,
                    price=float(post_data['price']),
                    description=post_data['description'],
                    category=Category.objects.get(name=post_data['category']),
                    url=f'{uri.replace("/videos/", "")}'
                )
                messages.success(request, 'Video uploaded correctly, it will soon be visible')
                return HttpResponseRedirect(reverse_lazy('shop:course-list'))
            else:
                return render(request, 'shop/course/create.html', {'form': data})
        except OperationalError:
            pass  # happens when db doesn't exist yet

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_teacher

    def handle_no_permission(self):
        return render(request=self.request, template_name='shop/permission/not_a_teacher.html')


class CourseDelete(OwnershipMixin, DeleteView):
    model = Course
    template_name = 'shop/course/delete.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})

    def delete(self, request, *args, **kwargs):
        """
        Override delete function to delete the video also on vimeo servers
        """
        uri = f'/videos/{Course.objects.get(id=kwargs["pk"]).url}'
        client = vimeo.VimeoClient(
            token=f'{constants.ACCESS_TOKEN}',
            key=f'{constants.CLIENT_ID}',
            secret=f'{constants.CLIENT_SECRET}'
        )
        client.delete(uri)
        return super().delete(request, args, kwargs)


class CourseUpdate(OwnershipMixin, UpdateView):
    model = Course
    template_name = 'shop/course/update.html'
    form_class = CourseUpdateForm

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})


class CourseDetail(CheckPurchaseMixin, DetailView):
    model = Course
    template_name = 'shop/course/detail.html'

    def get_context_data(self, **kwargs):
        """
        Put some context variable to hide or show the add comment/review buttons
        """
        context = super().get_context_data(**kwargs)
        try:
            check_purchase = Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                                     buyer_id=self.request.user.id).exists()
            context['purchased'] = check_purchase
        except OperationalError:
            pass  # happens when db doesn't exist yet

        return context


class CourseList(FilterView):
    model = Course
    template_name = 'shop/course/list.html'
    filterset_class = CourseFilter


class CoursePurchase(AlreadyBoughtMixin, CreateView):
    model = Purchase
    template_name = 'shop/purchase/complete_purchase.html'
    success_url = reverse_lazy('homepage')
    form_class = PurchaseForm

    def form_valid(self, form):
        form.instance.buyer_id = self.request.user.id
        form.instance.course_bought_id = self.kwargs['pk']
        return super(CoursePurchase, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context['course'] = course
        return context


class AddCommentView(AddCommentCheckMixin, CreateView):
    model = Comment
    template_name = 'shop/comment/add_comment.html'
    form_class = AddCommentForm

    def get_success_url(self):
        """
        This function provides the success url to go back to the commented course page
        """
        return reverse_lazy('shop:course-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course_id = self.kwargs['pk']
        return super(AddCommentView, self).form_valid(form)


class AddReplyView(CreateView):
    model = CommentReply
    template_name = 'shop/comment/add_reply.html'
    form_class = AddReplyForm

    def get_success_url(self):
        """
        This function provides the success url to go back to the commented course page
        """
        return reverse_lazy('shop:course-detail', kwargs={'pk': self.kwargs['course']})

    def form_valid(self, form):
        form.instance.reply_user = self.request.user
        form.instance.comment_id = self.kwargs['pk']
        return super(AddReplyView, self).form_valid(form)


class AddReviewView(ReviewChecksMixin, CreateView):
    model = Review
    template_name = 'shop/review/add_review.html'
    form_class = AddReviewForm

    def get_success_url(self):
        """
        This function provides the success url to go back to the commented course page
        """
        return reverse_lazy('shop:course-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.course_id = self.kwargs['pk']
        return super(AddReviewView, self).form_valid(form)
