import logging

import vimeo
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django_filters.views import FilterView

import constants
from filters import CourseFilter
from shop.forms import CourseForm, PurchaseForm, AddCommentForm, CourseUploadForm, CourseUpdateForm, AddReviewForm
from shop.mixins import OwnershipMixin, CheckPurchaseMixin
from shop.models import Course, Purchase, Comment, Review

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
        return self.request.user.is_authenticated and self.request.user.is_teacher

    def handle_no_permission(self):
        return render(request=self.request, template_name='shop/permission/not_a_teacher.html')


class CreateViewVimeo(UserPassesTestMixin, LoginRequiredMixin, View):
    form_class = CourseUploadForm
    template_name = 'shop/course/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        data = self.form_class(request.POST, request.FILES)
        post_data = request.POST

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
                url=f'{uri.replace("/videos/", "")}'
            )
            return HttpResponseRedirect(reverse_lazy('shop:course-list'))
        else:
            return render(request, 'shop/course/create.html', {'form': data})

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


class CourseList(FilterView):
    model = Course
    template_name = 'shop/course/list.html'
    filterset_class = CourseFilter


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['pk'])
        context['course'] = course
        return context


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


class AddReviewView(CheckPurchaseMixin, CreateView):
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
