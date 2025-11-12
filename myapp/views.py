# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.core.paginator import Paginator

#  only import the form you actually have
from .forms import CustomUserCreationForm

#  import only the models you still use
from .models import (
    Category,
    Course,
    Course_detail,
    Module,
    Quiz,
    Enrollment,
    Question,
    Option,
    Wishlist,
    SuggestedCourse,
)

# -------- Home --------
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    # Get suggested courses
    suggested_courses = SuggestedCourse.objects.select_related("course").all()
    
    # Get regular courses (excludes suggested ones via VisibleCourseManager)
    courses = Course.objects.all()
    categories = Category.objects.all()

    paginator = Paginator(courses, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {
        "courses": page_obj.object_list,
        "page_obj": page_obj,
        "categories": categories,
        "suggested_courses": suggested_courses,
    })

# -------- Auth --------
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

# -------- Category listing (public) --------
def category_courses(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Course_detail has M2M to Category via related_name="courses"
    course_details = category.courses.select_related("course").all()
    courses = [cd.course for cd in course_details]

    paginator = Paginator(courses, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "category_courses.html", {
        "category": category,
        "courses": page_obj.object_list,
        "page_obj": page_obj,
    })

# -------- Course Detail --------
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.all()
    enrolled = False
    wishlisted = False

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user, course=course, is_active=True
        ).exists()
        wishlisted = Wishlist.objects.filter(
            user=request.user, course=course
        ).exists()

    return render(request, "course_detail.html", {
        "course": course,
        "modules": modules,
        "enrolled": enrolled,
        "wishlisted": wishlisted,
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
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if not created and not enrollment.is_active:
        enrollment.is_active = True
        enrollment.save()
    return redirect("course_detail", slug=course.slug)

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

# -------- Quiz --------
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

        score = int((correct / total) * 100) if total > 0 else 0
        return render(request, "modules/quiz_result.html", {
            "quiz": quiz,
            "total": total,
            "correct": correct,
            "score": score,
            "user_answers": user_answers,
        })

    return render(request, "modules/quiz_detail.html", {"quiz": quiz, "questions": questions})

# -------- Wishlist --------
from django.views.decorators.http import require_POST

@login_required
@require_POST
def add_to_wishlist(request, slug):
    course = get_object_or_404(Course, slug=slug)
    Wishlist.objects.get_or_create(user=request.user, course=course)
    # simple redirect flow (no JS)
    return redirect("course_detail", slug=slug)

@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user).select_related("course")
    return render(request, "wishlist.html", {"items": items})

@login_required
@require_POST
def remove_from_wishlist(request, slug):
    course = get_object_or_404(Course, slug=slug)
    Wishlist.objects.filter(user=request.user, course=course).delete()
    return redirect("wishlist_page")


# -------- Manage Suggested Courses --------
@staff_member_required
def manage_suggested_courses(request):
    """View to list and manage suggested courses - Staff only"""
    suggested_courses = SuggestedCourse.objects.select_related("course").all()
    # Get courses that are not yet suggested (using all_objects to bypass the manager)
    available_courses = Course.all_objects.filter(suggestedcourse__isnull=True)
    
    return render(request, "manage/suggested_courses.html", {
        "suggested_courses": suggested_courses,
        "available_courses": available_courses,
    })

@staff_member_required
@require_POST
def add_suggested_course(request):
    """Add a course to the suggested section - Staff only"""
    course_id = request.POST.get("course_id")
    order = request.POST.get("order", 0)
    
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        SuggestedCourse.objects.create(course=course, order=order)
        messages.success(request, f"'{course.title}' has been added to suggested courses.")
    else:
        messages.error(request, "Please select a course.")
    
    return redirect("manage_suggested_courses")

@staff_member_required
@require_POST
def remove_suggested_course(request, suggestion_id):
    """Remove a course from the suggested section - Staff only"""
    suggestion = get_object_or_404(SuggestedCourse, id=suggestion_id)
    course_title = suggestion.course.title
    suggestion.delete()
    messages.success(request, f"'{course_title}' has been removed from suggested courses.")
    return redirect("manage_suggested_courses")


# -------- Manage Categories --------
@staff_member_required
def manage_categories(request):
    """View to list all categories - Staff only"""
    categories = Category.objects.all()
    return render(request, "manage/categories/list.html", {
        "categories": categories,
    })

@staff_member_required
def create_category(request):
    """View to create a new category - Staff only"""
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            messages.success(request, f"Category '{name}' has been created.")
            return redirect("manage_categories")
        else:
            messages.error(request, "Please enter a category name.")
    
    return render(request, "manage/categories/form.html", {
        "title": "Create Category",
    })

@staff_member_required
def update_category(request, pk):
    """View to update an existing category - Staff only"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            category.name = name
            category.save()
            messages.success(request, f"Category '{name}' has been updated.")
            return redirect("manage_categories")
        else:
            messages.error(request, "Please enter a category name.")
    
    return render(request, "manage/categories/form.html", {
        "title": "Update Category",
        "category": category,
    })

@staff_member_required
def delete_category(request, pk):
    """View to delete a category - Staff only"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == "POST":
        category_name = category.name
        category.delete()
        messages.success(request, f"Category '{category_name}' has been deleted.")
        return redirect("manage_categories")
    
    return render(request, "manage/categories/confirm_delete.html", {
        "category": category,
    })

@staff_member_required
def manage_category_courses(request, pk):
    """View to manage courses in a category - Staff only"""
    category = get_object_or_404(Category, pk=pk)
    
    # Get all course details that belong to this category
    category_course_details = category.courses.select_related("course").all()
    category_course_ids = [cd.course.id for cd in category_course_details]
    
    # Get all courses that are NOT in this category
    all_courses = Course.all_objects.all()
    available_courses = []
    
    for course in all_courses:
        # Check if course has details
        if hasattr(course, 'details'):
            if course.id not in category_course_ids:
                available_courses.append(course)
    
    return render(request, "manage/categories/manage_courses.html", {
        "category": category,
        "category_courses": category_course_details,
        "available_courses": available_courses,
    })

@staff_member_required
@require_POST
def add_course_to_category(request, pk):
    """Add a course to a category - Staff only"""
    category = get_object_or_404(Category, pk=pk)
    course_id = request.POST.get("course_id")
    
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        if hasattr(course, 'details'):
            category.courses.add(course.details)
            messages.success(request, f"'{course.title}' has been added to category '{category.name}'.")
        else:
            messages.error(request, f"Course '{course.title}' has no details and cannot be added to a category.")
    else:
        messages.error(request, "Please select a course.")
    
    return redirect("manage_category_courses", pk=pk)

@staff_member_required
@require_POST
def remove_course_from_category(request, pk, course_detail_id):
    """Remove a course from a category - Staff only"""
    category = get_object_or_404(Category, pk=pk)
    course_detail = get_object_or_404(Course_detail, id=course_detail_id)
    
    category.courses.remove(course_detail)
    messages.success(request, f"'{course_detail.course.title}' has been removed from category '{category.name}'.")
    
    return redirect("manage_category_courses", pk=pk)
