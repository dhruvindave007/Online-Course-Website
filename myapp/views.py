from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import Course


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


def header(request):
    return render(request, 'header.html')


def footer(request):
    return render(request, 'footer.html')


def courses(request):
    return render(request, 'courses.html')


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, 'course_detail.html', {'course': course})


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
