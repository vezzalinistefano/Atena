from django.contrib import admin

from shop.models import Course, Purchase, Comment, Category

# Register your models here.
admin.site.register(Course)
admin.site.register(Purchase)
admin.site.register(Comment)
admin.site.register(Category)
