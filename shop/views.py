from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from shop.forms import CourseForm, PurchaseForm
from shop.mixins import OwnershipMixin
from shop.models import Course, Purchase


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


class CourseDetail(DetailView):
    model = Course
    template_name = 'shop/course/detail.html'


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
