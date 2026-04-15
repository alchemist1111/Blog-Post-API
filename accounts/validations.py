import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# User registration validations
# Validate full name
def validate_full_name(value):
    """Validates the full name field for user registration and profile updates."""
    if value == " ":
        raise ValidationError("Full name cannot be empty.")
    if len(value) < 8:
        raise ValidationError("Full name must be at least 8 characters long.")
    if len(value) > 255:
        raise ValidationError("Full name cannot exceed 255 characters.")
    if not all(x.isalpha() or x.isspace() for x in value):
        raise ValidationError("Full name can only contain letters and spaces.")
    return value

# Validate email
def validate_email(value):
    """Validate that the email is not empty, proper format, and unique."""
    
    # Check for empty email
    if value == " ":
        raise ValidationError("Email cannot be empty.") # Email cannot be empty
    
    # Validate email format
    email_validator = EmailValidator()
    try:
        email_validator(value)
    except ValidationError:
        raise ValidationError("Invalid email format.") # Email must be in a valid format
    
    # Check for uniqueness
    if User.objects.filter(email=value).exists():
        raise ValidationError("Email is already in use.") # Email must be unique
    
    return value


# Validate password
def validate_password(value):
    """Validate that the password is not empty, meets complexity requirements, and is of valid length."""
    
    # Check for empty password
    if value == " ":
        raise ValidationError("Password cannot be empty.") # Password cannot be empty
    
    # Cjeck for minimum length
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.") # Password must be at least 8 characters long
    
    # Check for maximum length
    if len(value) > 128:
        
        raise ValidationError("Password cannot exceed 128 characters.") # Password cannot exceed 128 characters
    
    # Check for complexity (at least one uppercase, one lowercase, one digit, and one special character)
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Password must contain at least one uppercase letter.") # Password must contain at least one uppercase letter
    if not re.search(r'[a-z]', value):
        raise ValidationError("Password must contain at least one lowercase letter.") # Password must contain at least one lowercase letter
    if not re.search(r'[1-9]', value):
        raise ValidationError("Password must contain at least one digit.") # Password must contain at least one digit
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("Password must contain at least one special character.") # Password must contain at least one special character
    
    return value

# Password confirmation validation
def validate_password_confirmation(password, password_confirmation):
    """Validate that the password confirmation matches the original password."""
    if password != password_confirmation:
        raise ValidationError("Password confirmation does not match the original password.") # Password confirmation must match the original password
    return password_confirmation

# Validate password cannot be the same as full name or email
def validate_password_not_same_as_personal_info(password, full_name, email):
    """Validate that the password cannot be the same as the user's full name or email."""
    if password == full_name:
        raise ValidationError("Password cannot be the same as the full name.") # Password cannot be the same as the full name
    if password == email:
        raise ValidationError("Password cannot be the same as the email.") # Password cannot be the same as the email
    return password


# User profile validations
# Validate display name
def validate_display_name(value):
    """Validates the display name field for user profile updates."""
    if value and len(value) > 255:
        raise ValidationError("Display name cannot exceed 255 characters.") # Display name cannot exceed 255 characters
    return value

# Validate bio
def validate_bio(value):
    """Validates the bio field for user profile updates."""
    if value and len(value) > 1000:
        raise ValidationError("Bio cannot exceed 1000 characters.") # Bio cannot exceed 1000 characters
    return value

# Validate website URL
def validate_website(value):
    """Validates the website URL field for user profile updates."""
    if value and not re.match(r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$', value):
        raise ValidationError("Invalid website URL format.") # Website URL must be in a valid format
    return value

# Validate social media URLs
def validate_social_media_url(value):
    """Validates the social media URL fields for user profile updates."""
    if value and not re.match(r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$', value):
        raise ValidationError("Invalid social media URL format.") # Social media URL must be in a valid format
    return value

# Validate avatar image
def validate_avatar(image):
    """Validates the avatar image field for user profile updates."""
    if image:
        if image.size > settings.MAX_AVATAR_SIZE:
            raise ValidationError("Avatar image size cannot exceed 2MB.") # Avatar image size cannot exceed 2MB
        if not image.content_type in settings.ALLOWED_AVATAR_TYPES:
            raise ValidationError("Invalid avatar image format. Allowed formats: JPEG, PNG, GIF.") # Invalid avatar image format. Allowed formats: JPEG, PNG, GIF
    return image

# Validate no email change on profile update
def validate_no_email_change(instance, value):
    """Validates that the email cannot be changed during profile updates."""
    if instance.email != value:
        raise ValidationError("Email cannot be changed once set.") # Email cannot be changed during profile updates
    return value
    