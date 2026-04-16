from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, PostImage, Category, Tag, Comment, Like, Bookmark
from .filters import PostFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdmin, IsCommentAuthorOrAdmin
import logging
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostWriteSerializer,
    PostImageSerializer,
    CommentSerializer,
    LikeSerializer,
    BookmarkSerializer,
)

# Configure logging
logger = logging.getLogger(__name__)


# Category Views
class CategoryListView(APIView):
    """List all categories. Admin can create new categories."""
    serializer_class = CategorySerializer
   
    # Permissions: GET - AllowAny, POST - IsAuthenticated & IsAdminUser 
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    # Get all categories
    def get(self, request):
       try:
           categories = Category.objects.all()
           serializer = self.serializer_class(categories, many=True)
           success_message = {
                'success': True,
                'message': 'Categories retrieved successfully.',
                'data': serializer.data
           } 
           logger.info("Categories retrieved successfully.")
           return Response(success_message, status=status.HTTP_200_OK)
       except Exception as e:
           logger.error(f"An error occurred while retrieving categories: {str(e)}")
           exception_error_message = {
                'success': False,
                'message': f'An error occurred while retrieving categories: {str(e)}',
                'data': None
           }
           return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Create a new category
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                category = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Category created successfully.',
                    'data': self.serializer_class(category).data
                }
                logger.info("Category created successfully.")
                return Response(success_message, status=status.HTTP_201_CREATED)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for category creation.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while creating the category: {str(e)}',
                'data': None
            }       
            logger.error(f"An error occurred while creating the category: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Category Detail View
class CategoryDetailView(APIView):
    """Retrieve, update, or delete a category. Admin only for write operations."""
    serializer_class = CategorySerializer
    
    # Permissions: GET - AllowAny, PUT/DELETE - IsAuthenticated & IsAdminUser
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    # Helper method to get category object by slug
    def get_object(self, slug):
        return get_object_or_404(Category, slug=slug) 
    
    # Retrieve category details
    def get(self, request, slug):
        try:
            category = self.get_object(slug)
            serializer = self.serializer_class(category)
            success_message = {
                'success': True,
                'message': 'Category retrieved successfully.',
                'data': serializer.data
            }
            logger.info("Category retrieved successfully.")
            return Response(success_message, status=status.HTTP_200_OK)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while retrieving the category: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while retrieving the category: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Full update category details
    def put(self, request, slug):
        try:
            category = self.get_object(slug)
            serializer = self.serializer_class(category, data=request.data)
            if serializer.is_valid():
                category = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Category updated successfully.',
                    'data': self.serializer_class(category).data
                }
                logger.info("Category updated successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for category update.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while updating the category: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while updating the category: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Partial update category details
    def patch(self, request, slug):
        try:
            category = self.get_object(slug)
            serializer = self.serializer_class(category, data=request.data, partial=True)
            if serializer.is_valid():
                category = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Category partially updated successfully.',
                    'data': self.serializer_class(category).data
                }
                logger.info("Category partially updated successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for category partial update.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while partially updating the category: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while partially updating the category: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Delete a category
    def delete(self, request, slug):
        try:
            category = self.get_object(slug)
            category.delete()
            success_message = {
                'success': True,
                'message': 'Category deleted successfully.',
                'data': None
            }
            logger.info("Category deleted successfully.")
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while deleting the category: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while deleting the category: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                       

