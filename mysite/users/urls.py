# users/views.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('active/<active_code>', views.active_user, name='active_user'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
    path('forget_pwd_url/<active_code>', views.forget_pwd_url, name='forget_pwd_url'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.edit_users, name='edit'),
    path('activate_account/', views.register, name='activate_account'),
    path('invalid_link/', views.active_user, name='invalid_link'),
    path('pending_activation/', views.register, name='pending_activation'),
    path('message_profile/', views.message_profile, name='message_profile'),
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    path('users/<str:username>/followers/', views.followers, name='followers_list'),
    path('users/my_followers/', views.my_followers, name='my_followers'),  # 当前用户的粉丝列表
]
