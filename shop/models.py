from django.db import models

from users.models import UserProfile


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('Sport', 'Sport'),
        ('Finance', 'Finance'),
        ('Software Development', 'Software development'),
        ('Cooking', 'Cooking'),
        ('Health', 'Health'),
        ('Personal development', 'Personal development')
    ]

    MAX_LENGTH = 60
    MIN_LENGTH = 10

    title = models.CharField(max_length=MAX_LENGTH)
    teacher = models.ForeignKey(UserProfile,
                                related_name='teacher',
                                on_delete=models.PROTECT)
    price = models.FloatField(default=1.0)
    description = models.TextField()
    category = models.CharField(max_length=MAX_LENGTH,
                                choices=CATEGORY_CHOICES,
                                default='Misc')

    # TODO di che pacchetto fa parte il corso
    video = models.FileField(upload_to='courses/',
                             blank=True)
    url = models.URLField()

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        return f'{self.title} - {self.id}'


class Purchase(models.Model):
    buyer = models.ForeignKey(UserProfile,
                              related_name='purchases',
                              on_delete=models.PROTECT)
    course_bought = models.ForeignKey(Course,
                                      related_name='purchases',
                                      on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.buyer.username} - {self.course_bought.title}'


class Comment(models.Model):
    course = models.ForeignKey(Course,
                               related_name='comments',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,
                             related_name='comments',
                             on_delete=models.CASCADE)
    body = models.TextField(max_length=180,
                            verbose_name='Write down your thoughts:')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.title} - {self.user.username}'


