from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib import messages

# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect ('login')
    return render(request, 'home.html')

def header(request):
    return render(request, 'header.html')

def footer(request):
    return render(request, 'footer.html')

def courses(request):
    return render(request, 'courses.html')

def course_detail(request, course_id):
    # Assuming you have a Course model to fetch course details
    # course = get_object_or_404(Course, id=course_id)
    # return render(request, 'course_detail.html', {'course': course})
    return render(request, 'course_detail.html', {'course_id': course_id})  # Placeholder for now

def register_view(request):
    if request.method == 'POST':
        # form = RegistrationForm(request.POST)
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