from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import  AbstractUser

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='static/images/', default='static/images/default.png')
    slug = models.SlugField(unique=True, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)   # ✅ you had this in HTML
    created_at = models.DateTimeField(auto_now_add=True)

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

    # store as line-separated text
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

    def get_overview(self):
        return [line.strip() for line in self.overview.splitlines() if line.strip()]

    def get_outcomes(self):
        return [line.strip() for line in self.outcomes.splitlines() if line.strip()]

    def get_skills(self):
        return [line.strip() for line in self.skills.splitlines() if line.strip()]

    def get_tools(self):
        return [line.strip() for line in self.tools.splitlines() if line.strip()]

    def __str__(self):
        return f"Details for {self.course.title}"
