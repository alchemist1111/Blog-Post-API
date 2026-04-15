from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

# Class for the Base Custom User Manager
class UserManager(BaseUserManager):
    """"
        Custom user manager to handle user creation and soft deletion.
    """
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True) # Override the default queryset to exclude soft-deleted users
    
    # Create a regular user
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
     # Create a super user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
    # Soft delete
    def soft_delete(self, user):
        """Soft delete a user by setting deleted_at to the current timestamp."""
        user.deleted_at = timezone.now()
        user.save(update_fields=['deleted_at'])