from time import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CategoryForm, SuggestionForm
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import ListView, CreateView
from .models import (
    Category,
    Course,
    Module,
    Quiz,
    Enrollment,
    Question,
    Option,
    Wishlist,
    Suggestion,
)
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator


# -------- Home --------
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    # Show all courses on home (default manager returns all courses)
    courses = Course.objects.all()
    categories = Category.objects.all()
    suggested_courses = Suggestion.objects.select_related("course").all()

    # Pagination: 9 courses per page
    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {
            "courses": page_obj.object_list,
            "page_obj": page_obj,
            "categories": categories,
            "suggested_courses": suggested_courses,
        },
    )


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


def category_courses(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Get Course objects through Course_detail
    course_details = category.courses.select_related("course").all()
    courses = [cd.course for cd in course_details]
    # Pagination: 9 courses per page
    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "category_courses.html",
        {
            "category": category,
            "courses": page_obj.object_list,
            "page_obj": page_obj,
        },
    )


def suggested_courses(request):
    suggestions = Suggestion.objects.select_related("course").all()
    return render(
        request,
        "suggested_courses.html",
        {
            "suggestions": suggestions,
        },
    )


# -------- Course Detail --------
def course_detail(request, slug):
    # use default manager (objects) which now returns all courses
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.all()
    enrolled = False
    wishlisted = False

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user, course=course, is_active=True
        ).exists()
        wishlisted = Wishlist.objects.filter(user=request.user, course=course).exists()

    return render(
        request,
        "course_detail.html",
        {
            "course": course,
            "modules": modules,
            "enrolled": enrolled,
            "wishlisted": wishlisted,
        },
    )


# -------- Module List / Quiz --------
def module_list(request, course_slug):
    course = get_object_or_404(Course.objects, slug=course_slug)
    modules = course.modules.all()
    return render(
        request, "modules/module_test.html", {"course": course, "modules": modules}
    )


# -------- Enroll --------
@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course.objects, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if not created and not enrollment.is_active:
        enrollment.is_active = True
        enrollment.save()
    return redirect("course_detail", slug=course.slug)


@login_required
def toggle_enrollment_status(request, course_slug):
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course__slug=course_slug
    )
    enrollment.is_active = not enrollment.is_active
    enrollment.save()
    return JsonResponse({"status": "success", "is_active": enrollment.is_active})


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user, is_active=True)
    return render(request, "my_courses.html", {"enrollments": enrollments})


@login_required
def unenroll_course(request, course_slug):
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course__slug=course_slug
    )
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

        score = int((correct / total) * 100) if total > 0 else 0
        return render(
            request,
            "modules/quiz_result.html",
            {
                "quiz": quiz,
                "total": total,
                "correct": correct,
                "score": score,
                "user_answers": user_answers,
            },
        )

    return render(
        request, "modules/quiz_detail.html", {"quiz": quiz, "questions": questions}
    )


@login_required
@require_POST
def add_to_wishlist(request, slug):
    course = get_object_or_404(Course.objects, slug=slug)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, course=course
    )
    # If request is AJAX/Fetch, return JSON; otherwise redirect back to course page
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"created": created})
    # non-AJAX: redirect back
    return redirect("course_detail", slug=slug)


@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"items": items})


@login_required
@require_POST
def remove_from_wishlist(request, slug):
    course = get_object_or_404(Course.objects, slug=slug)
    deleted_count, _ = Wishlist.objects.filter(
        user=request.user, course=course
    ).delete()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"deleted_count": deleted_count})
    return redirect("course_detail", slug=slug)



def staff_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Permission denied.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    _wrapped.__name__ = view_func.__name__
    return _wrapped

# --- Category CRUD ---
@staff_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "manage/categories/list.html", {"categories": categories})

@staff_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created.")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, "manage/categories/form.html", {"form": form, "title": "Create Category"})

@staff_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, "manage/categories/form.html", {"form": form, "title": "Edit Category"})

@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted.")
        return redirect('category_list')
    return render(request, "manage/categories/confirm_delete.html", {"object": category, "title": "Delete Category"})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Suggestion
from .forms import SuggestionForm

def staff_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Permission denied.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    _wrapped.__name__ = view_func.__name__
    return _wrapped


# --- Manage Suggestions ---
@staff_required
def suggestion_list(request):
    suggestions = Suggestion.objects.select_related('main_course', 'suggested_course').all()
    return render(request, "manage/suggestions/list.html", {"suggestions": suggestions})

@staff_required
def suggestion_create(request):
    if request.method == "POST":
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Suggestion added successfully.")
            return redirect('suggestion_list')
    else:
        form = SuggestionForm()
    return render(request, "manage/suggestions/form.html", {"form": form, "title": "Add Suggestion"})

@staff_required
def suggestion_update(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if request.method == "POST":
        form = SuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            form.save()
            messages.success(request, "Suggestion updated.")
            return redirect('suggestion_list')
    else:
        form = SuggestionForm(instance=suggestion)
    return render(request, "manage/suggestions/form.html", {"form": form, "title": "Edit Suggestion"})

@staff_required
def suggestion_delete(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if request.method == "POST":
        suggestion.delete()
        messages.success(request, "Suggestion deleted.")
        return redirect('suggestion_list')
    return render(request, "manage/suggestions/confirm_delete.html", {"object": suggestion})
