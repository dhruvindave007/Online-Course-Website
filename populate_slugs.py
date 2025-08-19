from myapp.models import Course
from django.utils.text import slugify

def populate_slugs():
    courses = Course.objects.filter(slug__isnull=True)
    for course in courses:
        course.slug = slugify(course.title)
        course.save()
    print(f"Updated slugs for {courses.count()} courses.")

if __name__ == "__main__":
    populate_slugs()
