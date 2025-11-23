from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('complaint/<int:id>/', views.complaint_detail, name='complaint_detail'),
    path('after-login/', views.after_login, name='after_login'),
    path('profile/', views.profile, name='profile'),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-status/<int:id>/', views.update_status, name='update_status'),
    path('signup/', views.signup, name='signup'),

]
