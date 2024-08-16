# users/views.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('active<active_code>', views.active_user, name='active_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
]