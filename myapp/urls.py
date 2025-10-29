#urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("my-courses/", views.my_courses, name="my_courses"),

    # Courses
    path("category/<slug:slug>/", views.category_courses, name="category_courses"),
    path("suggested-courses/", views.suggested_courses, name="suggested_courses"),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path("course/<slug:course_slug>/modules/", views.module_list, name="module_list"),
    path("course/<slug:course_slug>/unenroll/", views.unenroll_course, name="unenroll_course"),
    path("course/<slug:course_slug>/toggle/", views.toggle_enrollment_status, name="toggle_enrollment_status"),

    # Quiz
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

    # Wishlist
    path('course/<slug:slug>/wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('course/<slug:slug>/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Category management
    path("manage/categories/", views.category_list, name="category_list"),
    path("manage/categories/create/", views.category_create, name="category_create"),
    path("manage/categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("manage/categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    # Manage suggestions (staff-only)
    path('manage/suggestions/', views.suggestion_list, name='suggestion_list'),
    path('manage/suggestions/add/', views.suggestion_create, name='suggestion_create'),
    path('manage/suggestions/<int:pk>/edit/', views.suggestion_update, name='suggestion_update'),
    path('manage/suggestions/<int:pk>/delete/', views.suggestion_delete, name='suggestion_delete'),


]