import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from shop.forms import CourseForm, PurchaseForm, AddCommentForm
from shop.mixins import OwnershipMixin, CheckPurchaseMixin
from shop.models import Course, Purchase, Comment

logger = logging.getLogger(__name__)


class CourseCreate(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Course
    template_name = 'shop/course/create.html'
    success_url = reverse_lazy('shop:course-list')
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.teacher_id = self.request.user.id
        return super(CourseCreate, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_teacher

    def handle_no_permission(self):
        return render(request=self.request, template_name='shop/permission/not_a_teacher.html')


class CourseDelete(OwnershipMixin, DeleteView):
    model = Course
    template_name = 'shop/course/delete.html'
    success_url = reverse_lazy('shop:course-list')


class CourseUpdate(OwnershipMixin, UpdateView):
    model = Course
    template_name = 'shop/course/update.html'
    fields = [
        'title',
        'price',
        'url',
        'description'
    ]
    success_url = reverse_lazy('shop:course-list')


class CourseDetail(CheckPurchaseMixin, DetailView):
    model = Course
    template_name = 'shop/course/detail.html'


class CourseList(ListView):
    model = Course
    template_name = 'shop/course/list.html'


class CoursePurchase(LoginRequiredMixin, CreateView):
    # TODO check if the user has already bought the course
    model = Purchase
    template_name = 'shop/purchase/complete_purchase.html'
    success_url = reverse_lazy('homepage')
    form_class = PurchaseForm

    def form_valid(self, form):
        form.instance.buyer_id = self.request.user.id
        form.instance.course_bought_id = self.kwargs['pk']
        return super(CoursePurchase, self).form_valid(form)


class SearchView(ListView):
    model = Course
    template_name = 'shop/search/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        print(query)
        if query:
            post_result = Course.objects.filter(title__contains=query)
            result = post_result
        else:
            result = None
        return result


class AddCommentView(CheckPurchaseMixin, CreateView):
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
