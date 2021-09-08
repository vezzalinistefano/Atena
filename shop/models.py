import requests
from django.db import models

from users.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    MAX_LENGTH = 60
    MIN_LENGTH = 3

    title = models.CharField(max_length=MAX_LENGTH)
    teacher = models.ForeignKey(UserProfile,
                                related_name='teacher',
                                on_delete=models.PROTECT)
    price = models.FloatField(default=1.0)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 related_name='courses',
                                 on_delete=models.CASCADE)

    # TODO di che pacchetto fa parte il corso
    video = models.FileField(upload_to='courses/',
                             blank=True)
    url = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    @property
    def get_thumbnail(self):
        response = requests.get(f"http://vimeo.com/api/v2/video/{self.url}.json")
        if response:
            print(response.text)
            data = response.json()

            return data[0]['thumbnail_medium']
        return "http://placehold.it/200X150"

    def __str__(self):
        return f'{self.title} - {self.id}'


class Purchase(models.Model):
    buyer = models.ForeignKey(UserProfile,
                              related_name='purchases',
                              on_delete=models.CASCADE)
    course_bought = models.ForeignKey(Course,
                                      related_name='purchases',
                                      on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.buyer.username} - {self.course_bought.title}'


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
    course = models.ForeignKey(Course,
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

    def __str__(self):
        return f'{self.user.username} - {self.date_added}'


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
    course = models.ForeignKey(Course,
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
