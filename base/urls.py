from django.urls import path

from .views import (
    dashboard, profile_list, profile, 
    login_page, logout_page, register_page,
    delete_tweet,
)


app_name = 'base'

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),

    path('', dashboard, name='dashboard'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>/', profile, name='profile'),

    path('delete/<int:id>', delete_tweet, name='delete'),
]