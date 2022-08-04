from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
     # reset password settings
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password/reset_password.html'), name='reset_password'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(template_name='password/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_done.html'), name='password_reset_complete'),
]