from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('header/', views.header, name='header'),
    path('footer/', views.footer, name='footer'),
]