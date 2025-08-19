from django.contrib import admin
from .models import Course, Course_detail



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Course_detail)
class CourseDetailAdmin(admin.ModelAdmin):
    list_display = ('course', 'instructor', 'language', 'updated_at')
