from django.contrib.auth.models import User
from django.db import models


class CreateMixin(models.Model):

    create_user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_user = request.user
        super().save_model(request, obj, form, change)
