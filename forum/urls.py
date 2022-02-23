from django.urls import path
from django.conf.urls.static import static

from core import settings
from forum.views import AddCommentView, AddReplyView, AddReviewView, UpdateReviewView

app_name = 'forum'

urlpatterns = [
    path('course/<int:course_pk>/comment', AddCommentView.as_view(), name='add-comment'),
    path('course/<int:course_pk>/<int:pk>/comment/reply', AddReplyView.as_view(), name='add-comment-reply'),
    path('course/<int:pk>/review', AddReviewView.as_view(), name='add-review'),
    path('course/<int:pk>/update-review', UpdateReviewView.as_view(), name='update-review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)