# import os
# import django

# # Set up Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') 
# django.setup()

# from myapp.models import Module, Quiz, Question, Option

# print("Starting to add quizzes to all modules...")

# for module in Module.objects.all():
#     quiz, created = Quiz.objects.get_or_create(
#         module=module,
#         title=f'{module.title} Quiz'
#     )
#     if created:
#         print(f"Created new quiz: '{quiz.title}'")

#     for i in range(1, 6):
#         question, created_q = Question.objects.get_or_create(
#             quiz=quiz,
#             text=f'Question {i} for {quiz.title}'
#         )
#         if created_q:
#             print(f"  - Created question: '{question.text}'")

#         Option.objects.get_or_create(
#             question=question,
#             text='Correct Option',
#             is_correct=True
#         )

#         for j in range(1, 4):
#             Option.objects.get_or_create(
#                 question=question,
#                 text=f'Incorrect Option {j}',
#                 is_correct=False
#             )

# print("Process finished.")

from myapp.models import Course, Module, Quiz, Question, Option
import random

# Sample data
module_titles = ["Introduction", "Intermediate Concepts", "Advanced Applications"]
quiz_titles = ["Basics Quiz", "Core Quiz", "Final Quiz"]
sample_questions = [
    ("What is the output of 2 + 2 in Python?", ["3", "4", "5", "22"], "4"),
    ("Which keyword defines a function in Python?", ["func", "def", "function", "lambda"], "def"),
    ("What does HTML stand for?", ["Hyper Trainer Marking Language", "Hyper Text Markup Language", "Hyper Text Making Language", "High Text Markup Language"], "Hyper Text Markup Language"),
    ("Which is not a programming language?", ["Python", "Java", "HTML", "C++"], "HTML"),
    ("Which data structure uses FIFO?", ["Stack", "Queue", "Tree", "Graph"], "Queue"),
    ("What does CSS stand for?", ["Cascading Style Sheets", "Computer Styled Sections", "Creative Style System", "Colorful Style Sheets"], "Cascading Style Sheets"),
    ("What is the capital of France?", ["Berlin", "Madrid", "Paris", "Rome"], "Paris"),
    ("Which one is an OOP concept?", ["Encapsulation", "Iteration", "Recursion", "Compilation"], "Encapsulation"),
]

for course in Course.objects.all():
    print(f"📘 Adding modules/quizzes/questions for course: {course.title}")

    for i, module_title in enumerate(module_titles, start=1):
        module, created = Module.objects.get_or_create(
            course=course,
            title=f"{module_title} - {course.title}",
            defaults={"description": f"This is the {module_title.lower()} for {course.title}."}
        )

        quiz, created = Quiz.objects.get_or_create(
            module=module,
            title=f"{quiz_titles[i-1]} - {course.title}"
        )

        # Add 5 random questions
        for q_num in range(5):
            q_text, options, correct = random.choice(sample_questions)
            question = Question.objects.create(quiz=quiz, text=q_text)

            for opt in options:
                Option.objects.create(
                    question=question,
                    text=opt,
                    is_correct=(opt == correct)
                )

print("✅ Modules, quizzes, questions & options added successfully!")
