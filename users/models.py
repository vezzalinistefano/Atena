from django.contrib.auth.models import User, AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True)
    user_photo = models.ImageField(upload_to='profiles/photos',
                                   verbose_name='Profile picture',
                                   default='media/profiles/photos/default/img.png')
    is_teacher = models.BooleanField(default=False,
                                     verbose_name='Do yo want to be a teacher?')
    bio = models.TextField(default='',
                           blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
