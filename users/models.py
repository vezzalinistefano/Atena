from django.db import models

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    short_bio = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
