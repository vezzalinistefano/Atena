import requests
from django.db import models

from forum.models import Review
from users.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'categories'


class Course(models.Model):
    MAX_LENGTH = 60
    MIN_LENGTH = 3

    title = models.CharField(max_length=MAX_LENGTH)
    teacher = models.ForeignKey(UserProfile,
                                related_name='courses',
                                on_delete=models.PROTECT)
    price = models.FloatField(default=1.0)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 related_name='courses',
                                 on_delete=models.CASCADE)
    url = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def check_if_teacher(self, user_id):
        return self.teacher_id == user_id

    @property
    def get_thumbnail(self):
        response = requests.get(f"http://vimeo.com/api/v2/video/{self.url}.json")
        if response:
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

    @property
    def get_user_review(self):
        review = Review.objects.get(
            course=self.course_bought,
            author=self.buyer
        )
        return review.pk
