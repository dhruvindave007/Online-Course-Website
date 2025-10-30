# models.py
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# ---------------------
# Manager that hides suggested courses from default queries
# ---------------------
class VisibleCourseManager(models.Manager):
    """
    Default manager: returns courses that are NOT suggested.
    So Course.objects.all() will not include suggested courses.
    Use Course.all_objects to access all courses (including suggested).
    """
    def get_queryset(self):
        return super().get_queryset().filter(suggestion__isnull=True)


# -------- User --------
class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)

# -------- Courses --------
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='static/images/', default='static/images/default.png')
    slug = models.SlugField(unique=True, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # default manager: only non-suggested courses (so "all courses" section won't include suggested ones)
    objects = VisibleCourseManager()
    # full manager if you ever need to access everything (including suggested)
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Course_detail(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="details", null=True, blank=True)
    instructor = models.CharField(max_length=255, null=True, blank=True)
    instructor_bio = models.TextField(blank=True)
    short_description = models.CharField(max_length=300)
    overview = models.TextField(blank=True)
    outcomes = models.TextField(blank=True, help_text="One outcome per line")
    skills = models.TextField(blank=True, help_text="One skill per line")
    tools = models.TextField(blank=True, help_text="One tool per line")
    requirements = models.TextField(blank=True)
    language = models.CharField(max_length=50, default="English")
    certificate = models.CharField(max_length=255, blank=True, null=True)
    languages_available = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateField(null=True, blank=True)
    exercises_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name="courses", blank=True)

    def __str__(self):
        return f"Details for {self.course.title}"


    def get_overview(self):
        return [line.strip() for line in self.overview.splitlines() if line.strip()]

    def get_outcomes(self):
        return [line.strip() for line in self.outcomes.splitlines() if line.strip()]

    def get_skills(self):
        return [line.strip() for line in self.skills.splitlines() if line.strip()]

    def get_tools(self):
        return [line.strip() for line in self.tools.splitlines() if line.strip()]

    def get_requirements(self):
        return [line.strip() for line in self.requirements.splitlines() if line.strip()]


    def __str__(self):
        return f"Details for {self.course.title}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Suggestion(models.Model):
    # one-to-one with Course: a course can be suggested at most once
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name="suggestion",
        null=True, blank=True, unique=True
    )

    def __str__(self):
        return f"Suggestion: {self.course.title}"



# -------- Module / Quiz / Question / Option --------
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules',blank=True, null=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} ({self.module.title})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# -------- Enrollment --------
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        status="Active" if self.is_active else "Inactive"
        return f"{self.user.username} - {self.course.title} ({status})"
    


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlists")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.username} wishlisted {self.course.title}"
