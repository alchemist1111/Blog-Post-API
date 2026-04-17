import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

# Set up user
User = get_user_model()

# This file is used to define fixtures that can be used across multiple test files.
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_user(db):
    user = User.objects.create_user(
        full_name = 'Test User',
        email = 'testuser@example.com',
        password = 'TestPassword@123',
        password_confirmation = 'TestPassword@123'
    )
    return user

@pytest.fixture
def auth_client(api_client, authenticated_user):
    api_client.force_authenticate(user=authenticated_user)
    return api_client