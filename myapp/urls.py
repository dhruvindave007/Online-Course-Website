# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-courses/', views.my_courses, name='my_courses'),

    # Category (public)
    path('category/<slug:slug>/', views.category_courses, name='category_courses'),

    # Courses
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<slug:course_slug>/modules/', views.module_list, name='module_list'),
    path('course/<slug:course_slug>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('course/<slug:course_slug>/toggle/', views.toggle_enrollment_status, name='toggle_enrollment_status'),

    # Quiz
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

    # Wishlist
    path('course/<slug:slug>/wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('course/<slug:slug>/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Management - Suggested Courses
    path('manage/suggested-courses/', views.manage_suggested_courses, name='manage_suggested_courses'),
    path('manage/suggested-courses/add/', views.add_suggested_course, name='add_suggested_course'),
    path('manage/suggested-courses/remove/<int:suggestion_id>/', views.remove_suggested_course, name='remove_suggested_course'),
    
    # Management - Categories
    path('manage/categories/', views.manage_categories, name='manage_categories'),
    path('manage/categories/create/', views.create_category, name='category_create'),
    path('manage/categories/update/<int:pk>/', views.update_category, name='category_update'),
    path('manage/categories/delete/<int:pk>/', views.delete_category, name='category_delete'),
    path('manage/categories/<int:pk>/courses/', views.manage_category_courses, name='manage_category_courses'),
    path('manage/categories/<int:pk>/courses/add/', views.add_course_to_category, name='add_course_to_category'),
    path('manage/categories/<int:pk>/courses/remove/<int:course_detail_id>/', views.remove_course_from_category, name='remove_course_from_category'),
]