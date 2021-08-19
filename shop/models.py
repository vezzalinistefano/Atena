from django.db import models

from users.models import UserProfile


class Course(models.Model):
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(UserProfile,
                                related_name='course',
                                on_delete=models.PROTECT)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    url = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} - {self.id}'
