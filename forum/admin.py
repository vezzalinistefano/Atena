from django.contrib import admin
from django.contrib.admin import ModelAdmin

from forum.models import Comment, Review, CommentReply


class CustomCommentAdmin(ModelAdmin):
    model = Comment
    list_display = ('user', 'course', 'date_added',)
    search_fields = ('user', 'course')


class CustomReviewAdmin(ModelAdmin):
    model = Review
    list_display = ('author', 'course', 'vote', 'date_added',)
    search_fields = ('user', 'course')


class CustomRepliesAdmin(ModelAdmin):
    model = CommentReply
    list_display = ('reply_user',)


admin.site.register(Comment, CustomCommentAdmin)
admin.site.register(Review, CustomReviewAdmin)
admin.site.register(CommentReply, CustomRepliesAdmin)
