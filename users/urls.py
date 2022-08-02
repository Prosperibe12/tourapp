from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('updateprofile/', views.updateprofile, name='updateprofile')
]