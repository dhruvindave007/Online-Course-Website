from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("my-courses/", views.my_courses, name="my_courses"),


    # Course
    path("category/<slug:slug>/", views.category_courses, name="category_courses"),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path("course/<slug:course_slug>/modules/", views.module_list, name="module_list"),
    path("course/<slug:course_slug>/unenroll/", views.unenroll_course, name="unenroll_course"),
    path("course/<slug:course_slug>/toggle/", views.toggle_enrollment_status, name="toggle_enrollment_status"),


    # Quiz
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),


]