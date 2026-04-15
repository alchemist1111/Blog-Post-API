from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import User, UserProfile
from .filters import UserFilter
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer, 
    UserAdminSerializer,
)
import logging

# Set up logging
logger = logging.getLogger(__name__)

# User registration view
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"New user registered: {user.email}")
                
                success_message = {
                    "message": "User registered successfully.",
                    "user": serializer.data
                }
                return Response(success_message, status=status.HTTP_201_CREATED)
            else:
                error_message = {
                    "message": "User registration failed.",
                    "errors": serializer.errors
                }
                logger.warning(f"User registration failed: {serializer.errors}")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                "message": "An error occurred during user registration.",
                "error": str(e)
            }
            logger.error(f"An error ocurred during user registration: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User login view
class UserLoginView(APIView):
    pass

# User retrieval view
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request):
        """Handle retrieval of the authenticated user's own details."""
        try:
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                error_message = {
                    "message": "Authentication credentials were not provided."
                }
                logger.warning("Authentication credentials were not provided.")
                return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
            else:
                user = request.user
                serializer = self.serializer_class(user)
            
                success_message = {
                    "message": "User details retrieved successfully.",
                    "user": serializer.data
                }
                logger.info(f"User details retrieved for: {user.email}")
                return Response(success_message, status=status.HTTP_200_OK)
            
        except Exception as e:
            exception_error_message = {
                "message": "An error occurred while retrieving user details.",
                "error": str(e)
            }
            logger.error(f"An error occurred while retrieving user details: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

# User update view
class UserUpdateView(APIView):
    """Handle full or partial update of the authenticated user's own details."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def put(self, request):
        """Handle full update of the authenticated user's own details."""
        serializer = self.serializer_class(request.user, data=request.data)
        
        try:
            if serializer.is_valid():
                user = serializer.save()
                success_message = {
                    "message": "User details updated successfully.",
                    "user": serializer.data
                }
                logger.info(f"User details updated for: {user.email}")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    "message": "User update failed.",
                    "errors": serializer.errors
                }
                logger.warning(f"User update failed: {serializer.errors}")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            exception_error_message = {
                "message": "An error occurred while updating user details.",
                "error": str(e)
            }
            logger.error(f"An error occurred while updating user details: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    def patch(self, request):
        """Handle partial update of the authenticated user's own details."""
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        
        try:
            if serializer.is_valid():
                user = serializer.save()
                
                success_message = {
                    "message": "User details partially updated successfully.",
                    "user": serializer.data
                }                    
                logger.info(f"User details partially updated for: {user.email}")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    "message": "User partial update failed.",
                    "errors": serializer.errors
                }
                logger.warning(f"User partial update failed: {serializer.errors}")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                "message": "An error occurred while partially updating user details.",
                "error": str(e)
            }
            logger.error(f"An error occurred while partially updating user details: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


# User soft delete view
class UserSoftDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        try:
            User.objects.soft_delete(request.user.id)
        
            success_message = {
                "message": "User account deleted successfully.",
                "user_id": str(request.user.id)
            }          
            logger.info(f"User account soft deleted: {request.user.email}")
            return Response(success_message, status=status.HTTP_200_OK)
        except Exception as e:
            exception_error_message = {
                "message": "An error occurred while deleting user account.",
                "error": str(e)
            }
            logger.error(f"An error occurred while deleting user account: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Admin Views
class AdminUserListView(APIView):
    """Admin only — list all users with filtering and pagination."""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    
    def get(self, request):
        # Use all_with_deleted so staff can filter by is_deleted too
        queryset = User.objects.all_with_deleted()
        
        # Apply filters
        try:
            filterset = UserFilter(request.GET, queryset=queryset)
            if not filterset.is_valid():    
                filter_error_message = {
                    "message": "Invalid filter parameters.",
                    "errors": filterset.errors
                }       
                logger.warning(f"Invalid filter parameters: {filterset.errors}")
                return Response(filter_error_message, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Apply pagination
                paginator = PageNumberPagination()
                paginated_queryset = paginator.paginate_queryset(filterset.qs, request)
                serializer = UserAdminSerializer(paginated_queryset, many=True)
                return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            exception_error_message = {
                "message": "An error occurred while retrieving user list.",
                "error": str(e)
            }
            logger.error(f"An error occurred while retrieving user list: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Admin user detail view
class AdminUserDetailView(APIView):
    """Admin only — retrieve any single user by ID, including soft-deleted ones."""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserAdminSerializer
    
    def get(self, request, pk):
        # Use all_with_deleted to allow retrieval of soft-deleted users
        try:
            user = get_object_or_404(User.objects.all_with_deleted(), pk=pk)
            serializer = self.serializer_class(user)
            success_message = {
                "message": "User details retrieved successfully.",
                "user": serializer.data
            }
            logger.info(f"Admin retrieved user details for: {user.email}")
            return Response(success_message, status=status.HTTP_200_OK)
        except Exception as e:
            exception_error_message = {
                "message": "An error occurred while retrieving user details.",
                "error": str(e)
            }
            logger.error(f"An error occurred while retrieving user details: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            