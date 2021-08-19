from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from shop.forms import CourseForm
from shop.models import Course


class CourseCreate(LoginRequiredMixin, CreateView):
    model = Course
    template_name = 'shop/course/create.html'
    success_url = reverse_lazy('shop:course-list')
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.teacher_id = self.request.user.id
        return super(CourseCreate, self).form_valid(form)


class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'shop/course/delete.html'
    success_url = reverse_lazy('shop:course-list')


class CourseUpdate(LoginRequiredMixin, UpdateView):
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
