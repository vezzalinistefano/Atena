from datetime import datetime

from django.db import models

from users.models import UserProfile


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('SP', 'Sport'),
        ('FN', 'Finance'),
        ('SWD', 'Software development'),
        ('CK', 'Cooking'),
        ('HL', 'Health'),
        ('PD', 'Personal development')
    ]

    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(UserProfile,
                                related_name='teacher',
                                on_delete=models.PROTECT)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    url = models.CharField(max_length=255)
    category = models.CharField(max_length=60,
                                choices=CATEGORY_CHOICES,
                                default='Misc')

    # TODO di che pacchetto fa parte il corso
    video = models.FileField(upload_to='courses/')

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        return f'{self.title} - {self.id}'


class Purchase(models.Model):
    buyer = models.ForeignKey(UserProfile,
                              related_name='buyer',
                              on_delete=models.PROTECT)
    course_bought = models.ForeignKey(Course,
                                      related_name='course_bought',
                                      on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, blank=True)
