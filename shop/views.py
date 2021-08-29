import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from shop.forms import CourseForm, PurchaseForm
from shop.mixins import OwnershipMixin
from shop.models import Course, Purchase

logger = logging.getLogger(__name__)


class CourseCreate(LoginRequiredMixin, CreateView):
    model = Course
    template_name = 'shop/course/create.html'
    success_url = reverse_lazy('shop:course-list')
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.teacher_id = self.request.user.id
        return super(CourseCreate, self).form_valid(form)


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


class CourseDetail(UserPassesTestMixin, DetailView):
    model = Course
    template_name = 'shop/course/detail.html'

    def test_func(self):
        return (Purchase.objects.filter(course_bought_id=self.kwargs['pk'],
                                        buyer_id=self.request.user.id).exists())

    def handle_no_permission(self):
        return render(request=self.request, template_name='permission_denied.html')


class CourseList(ListView):
    model = Course
    template_name = 'shop/course/list.html'


class CoursePurchase(LoginRequiredMixin, CreateView):
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
