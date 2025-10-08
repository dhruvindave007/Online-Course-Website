from django.contrib import admin
from .models import Course, Course_detail,  Module, Quiz, Question, Option, CustomUser, Category
from django.contrib.auth.admin import UserAdmin





@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Course_detail)
class CourseDetailAdmin(admin.ModelAdmin):
    list_display = ('course', 'instructor', 'language', 'updated_at','skills', 'tools', 'requirements')


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("contact",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("contact",)}),
    )


admin.site.register(Module)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
