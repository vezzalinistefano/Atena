from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from forum.forms import AddCommentForm, AddReplyForm, AddReviewForm, UpdateReviewForm
from forum.mixins import AddCommentCheckMixin, ReviewChecksMixin, ReviewUpdateMixin
from forum.models import Comment, CommentReply, Review


class AddCommentView(AddCommentCheckMixin, CreateView):
    model = Comment
    template_name = 'forum/comment/add_comment.html'
    form_class = AddCommentForm

    def get_success_url(self):
        """
        This function provides the success url to go back to the commented course page
        """
        return reverse_lazy('shop:course-detail', kwargs={'pk': self.kwargs['course_pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course_id = self.kwargs['course_pk']
        return super(AddCommentView, self).form_valid(form)


class AddReplyView(AddCommentCheckMixin, CreateView):
    model = CommentReply
    template_name = 'forum/comment/add_reply.html'
    form_class = AddReplyForm

    def get_success_url(self):
        """
        This function provides the success url to go back to the commented course page
        """
        return reverse_lazy('shop:course-detail', kwargs={'pk': self.kwargs['course_pk']})

    def form_valid(self, form):
        form.instance.reply_user = self.request.user
        form.instance.comment_id = self.kwargs['pk']
        return super(AddReplyView, self).form_valid(form)


class AddReviewView(ReviewChecksMixin, CreateView):
    model = Review
    template_name = 'forum/review/add_review.html'
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


class UpdateReviewView(ReviewUpdateMixin, UpdateView):
    model = Review
    template_name = 'forum/review/update_review.html'
    form_class = UpdateReviewForm

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})
