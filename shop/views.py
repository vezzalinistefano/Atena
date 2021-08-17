from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from shop.forms import CourseForm, TeacherProfileForm, form_validation_error
from shop.models import Course, TeacherProfile


class CourseCreate(LoginRequiredMixin, CreateView):
    template_name = 'shop/course/create.html'
    success_url = reverse_lazy('shop:course-list')
    form_class = CourseForm


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


class ProfileView(LoginRequiredMixin, View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = TeacherProfile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile}
        return render(request, 'author_profile/profile.html', context)

    def post(self, request):
        form = TeacherProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('blog:blogpost-profile')

