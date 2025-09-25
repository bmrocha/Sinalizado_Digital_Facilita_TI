from django.urls import path
from .views import (
    UserListCreateView, UserDetailView, ProfileView,
    login_view, logout_view, change_password_view
)

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]
