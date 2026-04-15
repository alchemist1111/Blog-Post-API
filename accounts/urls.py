from django.urls import path
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    UserDetailView, 
    UserUpdateView, 
    UserSoftDeleteView, 
    AdminUserListView, 
    AdminUserDetailView,
    UserProfileRetrieveView,
    UserProfileUpdateView,
)


url_patterns = [
    # User registration
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # User login
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # Authenticated user — self management
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('me/update/', UserUpdateView.as_view(), name='user-update'),
    path('me/delete/', UserSoftDeleteView.as_view(), name='user-soft-delete'),
    
    # Authenticated user — profile
    path('me/profile/', UserProfileRetrieveView.as_view(), name='user-profile-retrieve'),
    path('me/profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    
    # Admin user management
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<uuid:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
]