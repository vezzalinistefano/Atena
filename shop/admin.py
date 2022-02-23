from django.contrib import admin
from django.contrib.admin import ModelAdmin

from shop.models import Course, Purchase, Category


class CustomCourseAdmin(ModelAdmin):
    model = Course
    list_filter = ('category',)
    list_display = ('title', 'teacher', 'price', 'category')
    ordering = ('price',)
    search_fields = ('title', 'teacher', 'price', 'category')


class PurchaseCustomAdmin(ModelAdmin):
    model = Purchase
    list_display = ('buyer', 'course_bought', 'date')
    search_fields = ('buyer', 'course_bought')


admin.site.register(Course, CustomCourseAdmin)
admin.site.register(Purchase, PurchaseCustomAdmin)
admin.site.register(Category)
