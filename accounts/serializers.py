from rest_framework import serializers
from .models import User, UserProfile
from .validations import (
    validate_full_name,
    validate_email,
    validate_password,
    validate_password_confirmation,
    validate_password_not_same_as_personal_info,
    validate_display_name,
    validate_bio,
    validate_website,
    validate_social_media_url,
    validate_avatar,
    validate_no_email_change,
    
)

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'is_active', 'is_staff', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'is_active', 'is_staff', 'created_at', 'updated_at', 'deleted_at']
    
    # Validations
    # Validate full name
    def validate_full_name(self, value):
        return validate_full_name(value)
    
    # Validate email
    def validate_email(self, value):
        if self.instance:
            return validate_no_email_change(self.instance, value) # Prevent email change on profile update
        return validate_email(value)


# User admin 
class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'is_active', 'is_staff', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']     

# User registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password_confirmation']
    
    # Validations
    # Validate full name
    def validate_full_name(self, value):
        return validate_full_name(value)
    
    # Validate email
    def validate_email(self, value):
        return validate_email(value)
    
    # Validate password
    def validate_password(self, value):
        return validate_password(value)
    
    def validate(self, data):
        # Confirm passwords match
        validate_password_confirmation(
            data.get('password'),
            data.get('password_confirmation'),
        )
        # Confirm password does not mirror personal info
        validate_password_not_same_as_personal_info(
            data.get('password'),
            data.get('full_name'),
            data.get('email'),
        )
        # Return the validated data
        return data
    
    def create(self, validated_data):
        """Create a new user instance with hashed password."""
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save() 
        return user  

# User profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    """Used for retrieving the authenticated user's profile."""
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'email', 'display_name', 'bio', 'website', 'avatar', 'website', 'twitter', 'linkedin', 'github', 'created_at', 'updated_at',]
        read_only_fields = ['id', 'full_name', 'email', 'created_at', 'updated_at']

# User profile update serializer
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Used for updating the authenticated user's profile."""
    
    class Meta:
        model = UserProfile
        fields = ['display_name', 'bio', 'website', 'avatar', 'website', 'twitter', 'linkedin', 'github']
        
    # Validations
    # Validate display name
    def validate_display_name(self, value):
        return validate_display_name(value)
    
    # Validate bio
    def validate_bio(self, value):
        return validate_bio(value)
    
    # Validate website
    def validate_website(self, value):
        return validate_website(value)
    
    # validate avatar
    def validate_avatar(self, value):
        return validate_avatar(value)
    
    # validate twitter url
    def validate_twitter(self, value):
        return validate_social_media_url(value, 'twitter')  
    
    # validate linkedin url
    def validate_linkedin(self, value):
        return validate_social_media_url(value, 'linkedin')
    
    # validate github url
    def validate_github(self, value):
        return validate_social_media_url(value, 'github')  

# Forgot password serializer
class ForgotPasswordSerializer(serializers.Serializer):
    pass

# Reset password serializer
class ResetPasswordSerializer(serializers.Serializer):
    pass