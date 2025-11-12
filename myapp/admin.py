from django.contrib import admin
from .models import Course, Course_detail,  Module, Quiz, Question, Option, CustomUser, Category, SuggestedCourse
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

@admin.register(SuggestedCourse)
class SuggestedCourseAdmin(admin.ModelAdmin):
    list_display = ("course", "order", "created_at")
    search_fields = ("course__title",)
    list_editable = ("order",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            # Allow selecting only courses that don't have a suggestion yet.
            # If editing an existing SuggestedCourse, include the current course.
            if request.resolver_match.kwargs.get("object_id"):
                # editing existing suggestion: allow current course + others not suggested
                suggestion_obj = self.get_object(request, request.resolver_match.kwargs["object_id"])
                current_course_qs = Course.all_objects.filter(pk=suggestion_obj.course_id)
                others_qs = Course.all_objects.filter(suggestedcourse__isnull=True)
                kwargs["queryset"] = current_course_qs.union(others_qs)
            else:
                # creating: only courses that are not suggested
                kwargs["queryset"] = Course.all_objects.filter(suggestedcourse__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)






admin.site.register(Module)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)