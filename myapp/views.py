from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Category, Course, Module, Quiz, Enrollment, Question, Option
from django.http import JsonResponse


# -------- Home --------
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    courses = Course.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'courses': courses, 'categories': categories})


# -------- Auth --------
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def category_courses(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Get Course objects through Course_detail
    course_details = category.courses.select_related("course").all()
    courses = [cd.course for cd in course_details]

    return render(request, "category_courses.html", {
        "category": category,
        "courses": courses,
    })


# -------- Course Detail --------
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.all()
    enrolled = False

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(user=request.user, course=course, is_active=True).exists()

    return render(request, "course_detail.html", {
        "course": course,
        "modules": modules,
        "enrolled": enrolled,
    })

# -------- Module List / Quiz --------
def module_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    modules = course.modules.all()
    return render(request, "modules/module_test.html", {"course": course, "modules": modules})


# -------- Enroll --------
@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if not created and not enrollment.is_active:
        enrollment.is_active = True
        enrollment.save()
    return redirect('course_detail', slug=course.slug)


@login_required
def toggle_enrollment_status(request, course_slug):
    enrollment = get_object_or_404(Enrollment, user=request.user, course__slug=course_slug)
    enrollment.is_active = not enrollment.is_active
    enrollment.save()
    return JsonResponse({"status": "success", "is_active": enrollment.is_active})


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user, is_active=True)
    return render(request, "my_courses.html", {"enrollments": enrollments})


@login_required
def unenroll_course(request, course_slug):
    enrollment = get_object_or_404(Enrollment, user=request.user, course__slug=course_slug)
    enrollment.is_active = False
    enrollment.save()
    return redirect("my_courses")





def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  

    if request.method == "POST":
        total = questions.count()
        correct = 0
        user_answers = {}

        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")
            if selected_option_id:
                option = Option.objects.get(id=selected_option_id)
                user_answers[question.id] = option.id
                if option.is_correct:
                    correct += 1
            else:
                user_answers[question.id] = None

        score = int((correct / total) * 100)
        return render(request, "modules/quiz_result.html", {
            "quiz": quiz,
            "total": total,
            "correct": correct,
            "score": score,
            "user_answers": user_answers,
        })

    return render(request, "modules/quiz_detail.html", {"quiz": quiz, "questions": questions})
