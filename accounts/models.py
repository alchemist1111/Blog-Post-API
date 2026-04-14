from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser
from posts.models import TimeStampedModel
import uuid

# Custom User model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    objects = UserManager()
    
    class Meta:
        """Class for defining user table constraints and indexes"""
        
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_user_email')
        ]
        
        indexes = [
            models.Index(fields=['full_name'], name='user_full_name_idx'),
            models.Index(fields=['email'], name='user_email_idx'),
            models.Index(fields=['created_at'], name='user_created_at_idx'),
            models.Index(fields=['updated_at'], name='user_updated_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.full_name} <{self.email}>"  


# User Profile model
class UserProfile(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="user_profiles/avatars/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)       
    
    class Meta:
        db_table = 'user_profiles'
        
        ordering = ["display_name"]
        
    def __str__(self):
        return self.display_name if self.display_name else self.user.full_name