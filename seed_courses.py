from myapp.models import Course, Course_detail, Category
from django.utils.text import slugify
import random
from datetime import date

# Categories
categories_data = [
    "Computer Science",
    "Business Management",
    "Design & Creativity",
    "Health & Lifestyle",
]

categories = {}
for name in categories_data:
    category, _ = Category.objects.get_or_create(
        name=name,
        defaults={"slug": slugify(name)},
    )
    categories[name] = category

# Sample data
instructors = [
    ("Dr. Alice Johnson", "PhD in Computer Science, 10+ years teaching AI & ML."),
    ("Mr. Bob Smith", "Business consultant with 15 years of leadership experience."),
    ("Ms. Clara Green", "Award-winning designer, passionate about creative education."),
    ("Dr. David Brown", "Nutritionist and wellness expert for over 12 years."),
]

courses_data = {
    "Computer Science": [
        ("Python for Beginners", "Learn Python from scratch and build real projects."),
        ("Data Structures & Algorithms", "Master problem-solving with advanced algorithms."),
        ("Machine Learning Basics", "Introduction to ML concepts with hands-on projects."),
    ],
    "Business Management": [
        ("Project Management Essentials", "Learn to manage projects efficiently."),
        ("Entrepreneurship 101", "Build and grow your startup idea."),
        ("Leadership & Communication", "Develop skills to lead teams effectively."),
    ],
    "Design & Creativity": [
        ("Graphic Design Fundamentals", "Master Photoshop, Illustrator, and design principles."),
        ("UI/UX Design", "Learn how to design user-friendly digital products."),
        ("Video Editing Basics", "Edit professional videos with industry tools."),
    ],
    "Health & Lifestyle": [
        ("Yoga for Beginners", "Improve flexibility, balance, and mental clarity."),
        ("Healthy Eating Habits", "Learn nutrition fundamentals for daily life."),
        ("Stress Management Techniques", "Reduce stress with practical exercises."),
    ],
}

for cat_name, courses_list in courses_data.items():
    for title, desc in courses_list:
        course, created = Course.objects.get_or_create(
            title=title,
            defaults={
                "description": desc,
                "price": random.choice([499, 799, 999, 1499]),
                "duration": random.choice(["4 weeks", "6 weeks", "8 weeks"]),
                "start_date": date.today(),
            },
        )

        if created or not hasattr(course, "details"):
            instructor, bio = random.choice(instructors)
            detail = Course_detail.objects.create(
                course=course,
                instructor=instructor,
                instructor_bio=bio,
                short_description=desc,
                overview="This course provides in-depth training on " + title,
                outcomes="Understand fundamentals\nApply knowledge in projects\nBuild confidence",
                skills="Problem-solving\nCritical Thinking\nPractical Application",
                tools="Google Colab\n Jupyter Notebook\n Industry Software",
                requirements="Basic computer knowledge\nWillingness to learn",
                language="English",
                certificate="Certificate of Completion",
                languages_available="English, Hindi",
                exercises_count=random.randint(5, 15),
            )
            detail.categories.add(categories[cat_name])

print("✅ Courses & Categories seeded successfully!")
