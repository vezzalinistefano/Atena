from django.db import models

from users.models import UserProfile


class BaseComment(models.Model):
    body = models.TextField(max_length=180,
                            verbose_name='Write down your thoughts:')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Comment(BaseComment):
    user = models.ForeignKey(UserProfile,
                             related_name='comments',
                             on_delete=models.CASCADE)
    course = models.ForeignKey(to='shop.Course',
                               related_name='comments',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.title} - {self.user.username}'


class CommentReply(BaseComment):
    reply_user = models.ForeignKey(UserProfile,
                                   related_name='replies',
                                   on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,
                                related_name='replies',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Comment replies'

    def __str__(self):
        return f'{self.reply_user.username} - {self.date_added}'


class Review(models.Model):
    VOTE_CHOICES = (
        (1, 'Bad'),
        (2, 'Not that good'),
        (3, 'Nice'),
        (4, 'Very good'),
        (5, 'Perfect!')
    )
    author = models.ForeignKey(UserProfile,
                               related_name='reviews',
                               on_delete=models.CASCADE)
    course = models.ForeignKey(to='shop.Course',
                               related_name='reviews',
                               on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE_CHOICES,
                               default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=255)

    def __str__(self):
        return f''

    @property
    def get_vote(self):
        return self.VOTE_CHOICES[self.vote - 1][1]
