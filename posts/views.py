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


# Tag Views
class TagListView(APIView):
    """List all tags. Admin can create new tags."""
    serializer_class = TagSerializer
    
    # Permissions: GET - AllowAny, POST - IsAuthenticated & IsAdminUser
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()] 
    
    def get(self, request):
        try:
            tags = Tag.objects.all()
            serializer = self.serializer_class(tags, many=True)
            success_message = {
                'success': True,
                'message': 'Tags retrieved successfully.',
                'data': serializer.data
            }
            logger.info("Tags retrieved successfully.")
            return Response(success_message, status=status.HTTP_200_OK)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while retrieving tags: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while retrieving tags: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    # Create a new tag
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                tag = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Tag created successfully.',
                    'data': self.serializer_class(tag).data
                }
                logger.info("Tag created successfully.")
                return Response(success_message, status=status.HTTP_201_CREATED)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for tag creation.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while creating the tag: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while creating the tag: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Tag Detail View
class TagDetailView(APIView):
    """Retrieve, update, or delete a tag. Admin only for write operations."""
    serializer_class = TagSerializer
    
    # Permissions: GET - AllowAny, PUT/DELETE - IsAuthenticated & IsAdminUser
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    # Helper method to get tag object by slug
    def get_object(self, slug):
        return get_object_or_404(Tag, slug=slug)  
    
    # Retrieve tag details
    def get(self, request, slug):
        try:
            tag = self.get_object(slug)
            serializer = self.serializer_class(tag)
            success_message = {
                'success': True,
                'message': 'Tag retrieved successfully.',
                'data': serializer.data
            }
            logger.info("Tag retrieved successfully.")
            return Response(success_message, status=status.HTTP_200_OK)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while retrieving the tag: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while retrieving the tag: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Full update tag details
    def put(self, request, slug):
        try:
            tag = self.get_object(slug)
            serializer = self.serializer_class(tag, data=request.data)
            if serializer.is_valid():
                tag = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Tag updated successfully.',
                    'data': self.serializer_class(tag).data
                }
                logger.info("Tag updated successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for tag update.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while updating the tag: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while updating the tag: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Partial update tag details
    def patch(self, request, slug):
        try:
            tag = self.get_object(slug)
            serializer = self.serializer_class(tag, data=request.data, partial=True)
            if serializer.is_valid():
                tag = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Tag partially updated successfully.',
                    'data': self.serializer_class(tag).data
                }
                logger.info("Tag partially updated successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for tag partial update.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while partially updating the tag: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while partially updating the tag: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Delete a tag
    def delete(self, request, slug):
        try:
            tag = self.get_object(slug)
            tag.delete()
            success_message = {
                'success': True,
                'message': 'Tag deleted successfully.',
                'data': None
            }
            logger.info("Tag deleted successfully.")
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while deleting the tag: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while deleting the tag: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


# Post Views
class PostListView(APIView):
    """
        Public — list all published posts with filtering, search, and pagination.
        Authors see their own posts regardless of status.
    """ 
    permission_classes = [AllowAny]
    serialogizer_class = PostListSerializer
    
    def get(self, request):
        try:
            if request.user.is_authenticated:
                if request.user.is_staff:
                    # Admin can see all posts
                    queryset = Post.objects.all()
                else:
                    # Authors see published posts + their own posts of any status
                    queryset = Post.objects.filter(
                        status = Post.PostStatus.PUBLISHED
                    ) | Post.objects.filter(author=request.user) # Authors can see their own posts regardless of status
                    queryset = queryset.distinct() # Remove duplicates if any 
            else:
                # Unauthenticated users see published posts only
                queryset = Post.objects.filter(status=Post.PostStatus.PUBLISHED)
            
            # Apply filtering
            filter_backends = PostFilter(request.GET, queryset=queryset)
            if not filter_backends.is_valid():
                error_message = {
                    'success': False,
                    'message': 'Invalid filter parameters.',
                    'data': filter_backends.errors
                }
                logger.warning("Invalid filter parameters provided for post listing.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            
            # Apply pagination
            paginator = PageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(filter_backends.qs, request)
            
            serializer = self.serialogizer_class(paginated_queryset, many=True)
            success_message = {
                'success': True,
                'message': 'Posts retrieved successfully.',
                'data': serializer.data
            }
            logger.info("Posts retrieved successfully.")
            return paginator.get_paginated_response(success_message)
        
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while retrieving posts: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while retrieving posts: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Post Detail View
class PostDetailView(APIView):
    """
        Public — retrieve a single post by slug.
        Increments view count on each request.
    """ 
    permission_classes = [AllowAny]
    serializer_class = PostDetailSerializer
    
    # Helper method to get post object by slug
    def get_object(self, slug):
        return get_object_or_404(Post, slug=slug)
    
    # Retrieve post details
    def get(self, request, slug):
        try:
            if request.user.is_authenticated and request.user.is_staff:
                # Admin can see any post
                post = self.get_object(slug)
            elif request.user.is_authenticated:
                # Authors can see published posts + their own posts of any status
                post = get_object_or_404(
                    Post.objects.filter(
                        status=Post.PostStatus.PUBLISHED
                    ) | Post.objects.filter(author=request.user),
                    slug=slug
                )
            else:
                # Unauthenticated users see published posts only
                post = get_object_or_404(Post, slug=slug, status=Post.PostStatus.PUBLISHED)
            
            # Increment view count
            Post.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)  
            
            Serializer = self.serializer_class(post)
            success_message = {
                'success': True,
                'message': 'Post retrieved successfully.',
                'data': Serializer.data 
            }                 
            logger.info("Post retrieved successfully.")
            return Response(success_message, status=status.HTTP_200_OK)
        
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while retrieving the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while retrieving the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Post Create View
class PostCreateView(APIView):
    """Authenticated users can create posts."""
    permission_classes = [IsAuthenticated]
    serializer_class = PostWriteSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                post = serializer.save(author=request.user)
                success_message = {
                    'success': True,
                    'message': 'Post created successfully.',
                    'data': PostDetailSerializer(post).data
                }
                logger.info("Post created successfully.")
                return Response(success_message, status=status.HTTP_201_CREATED)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for post creation.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while creating the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while creating the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Post Update View
class PostUpdateView(APIView):
    """Authors can update their own posts. Admins can update any post."""                
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin] 
    serializer_class = PostWriteSerializer
    
    # Helper method to get post object by slug
    def get_object(self, slug):
        post = get_object_or_404(Post, slug=slug)
        self.check_object_permissions(self.request, post)  # Check permissions
        return post
    
    # Full update post details
    def put(self, request, slug):
        try:
            post = self.get_object(slug)
            serializer = self.serializer_class(post, data=request.data, context={'request': request})
            if serializer.is_valid():
                post = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Post updated successfully.',
                    'data': PostDetailSerializer(post).data
                }
                logger.info("Post updated successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for post update.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while updating the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while updating the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Partial update post details
    def patch(self, request, slug):
        try:
            post = self.get_object(slug)
            serializer = self.serializer_class(post, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                post = serializer.save()
                success_message = {
                    'success': True,
                    'message': 'Post partially updated successfully.',
                    'data': PostDetailSerializer(post).data
                }
                logger.info("Post partially updated successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for post partial update.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while partially updating the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while partially updating the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Post Delete View
class PostDeleteView(APIView):
    """Authors can delete their own posts. Admins can delete any post."""
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
    
    # Helper method to get post object by slug
    def get_object(self, slug):
        post = get_object_or_404(Post, slug=slug)
        self.check_object_permissions(self.request, post)
        return post
    
    # Delete a post
    def delete(self, request, slug):
        try:
            post = self.get_object(slug)
            post.delete()
            success_message = {
                'success': True,
                'message': 'Post deleted successfully.',
                'data': None
            }
            logger.info("Post deleted successfully.")
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while deleting the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while deleting the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Post Image views
class PostImageCreateView(APIView):
    """Authors can add images to their own posts. Admins can add to any post."""
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
    serializer_class = PostImageSerializer
    
    # Helper method to get post object by slug
    def get_object(self, slug):
        post = get_object_or_404(Post, slug=slug)
        self.check_object_permissions(self.request, post)
        return post
    
    
    # Create a new image for a post
    def post(self, request, slug):                                   
        try:
            post = self.get_object(slug)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                post_image = serializer.save(post=post)
                success_message = {
                    'success': True,
                    'message': 'Image added to post successfully.',
                    'data': self.serializer_class(post_image).data
                }
                logger.info("Image added to post successfully.")
                return Response(success_message, status=status.HTTP_201_CREATED)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for adding image to post.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while adding image to the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while adding image to the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Post Image Delete View
class PostImageDeleteView(APIView):
    """Authors can delete images from their own posts. Admins can delete from any post."""
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
    
    # Helper method to get post image object by id
    def get_object(self, slug):
        post = get_object_or_404(Post, slug=slug)
        self.check_object_permissions(self.request, post)
        return post
    
    # Delete an image from a post
    def delete(self, request, slug, image_id):
        try:
            post = self.get_object(slug)
            post_image = get_object_or_404(PostImage, id=image_id, post=post, context={'request': request})
            post_image.delete()
            success_message = {
                'success': True,
                'message': 'Image deleted from post successfully.',
                'data': None
            }
            logger.info("Image deleted from post successfully.")
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while deleting image from the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while deleting image from the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


# Comment views
class CommentListCreateView(APIView):
    """
        Public — list approved comments on a post.
        Authenticated users can create comments.
    """ 
    serializer_class = CommentSerializer
    
    # Permissions: GET - AllowAny, POST - IsAuthenticated
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]   
    
    # Helper method to get post object by slug
    def get(self, request, slug):  
        post = get_object_or_404(Post, slug=slug, status=Post.PostStatus.PUBLISHED)
        # Return only top-level comments; replies are nested inside
        comments = post.comments.filter(parent__is=True)
        serializer = self.serializer_class(comments, many=True)
        success_message = {
            'success': True,
            'message': 'Comments retrieved successfully.',
            'data': serializer.data
        }
        return Response(success_message, status=status.HTTP_200_OK) 
    
    # Create a new comment on a post
    def post(self, request, slug):
        try:
            post = get_object_or_404(Post, slug=slug, status=Post.PostStatus.PUBLISHED)
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                comment = serializer.save(post=post, author=request.user)
                success_message = {
                    'success': True,
                    'message': 'Comment created successfully.',
                    'data': self.serializer_class(comment).data
                }
                logger.info("Comment created successfully.")
                return Response(success_message, status=status.HTTP_201_CREATED)
            else:
                error_message = {
                    'success': False,
                    'message': 'The data provided is invalid.',
                    'data': serializer.errors
                }
                logger.warning("Invalid data provided for comment creation.")
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while creating the comment: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while creating the comment: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# comment delete view
class CommentDeleteView(APIView):
    """Comment authors can delete their own comments. Admins can delete any comment."""
    permission_classes = [IsAuthenticated, IsCommentAuthorOrAdmin]
    
    # Helper method to get comment object by id
    def get_object(self, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        self.check_object_permissions(self.request, comment)
        return comment
    
    # Delete a comment
    def delete(self, request, slug, comment_id):
        try:
            comment = self.get_object(comment_id)
            comment.delete()
            success_message = {
                'success': True,
                'message': 'Comment deleted successfully.',
                'data': None
            }
            logger.info("Comment deleted successfully.")
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while deleting the comment: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while deleting the comment: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Like views
class LikeToggleView(APIView):
    """Toggle like on a post. Like if not liked, unlike if already liked."""
    permission_classes = [IsAuthenticated]
    
    # Create or delete a like for a post
    def post(self, request, slug):
        try:
            post = get_object_or_404(Post, slug=slug, status=Post.PostStatus.PUBLISHED)
            like, created = Like.objects.get_or_create(post=post, user=request.user)
            if not created:
                like.delete()
                success_message = {
                    'success': True,
                    'message': 'Post unliked successfully.',
                    'data': None
                }
                logger.info("Post unliked successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                success_message = {
                    'success': True,
                    'message': 'Post liked successfully.',
                    'data': None
                }
                logger.info("Post liked successfully.")
                return Response(success_message, status=status.HTTP_201_CREATED)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while toggling like on the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while toggling like on the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Bookmark views
class BookmarkToggleView(APIView):
    """Toggle bookmark on a post. Bookmark if not bookmarked, remove if already bookmarked."""
    permission_classes = [IsAuthenticated]
    
    # Create or delete a bookmark for a post
    def post(self, request, slug):
        try:
            post = get_object_or_404(Post, slug=slug, status=Post.PostStatus.PUBLISHED)
            bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
            if not created:
                bookmark.delete()
                success_message = {
                    'success': True,
                    'message': 'Post removed from bookmarks successfully.',
                    'data': None
                }
                logger.info("Post removed from bookmarks successfully.")
                return Response(success_message, status=status.HTTP_200_OK)
            else:
                success_message = {
                    'success': True,
                    'message': 'Post bookmarked successfully.',
                    'data': None
                }
                logger.info("Post bookmarked successfully.")
                return Response(success_message, status=status.HTTP_201_CREATED)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while toggling bookmark on the post: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while toggling bookmark on the post: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Bookmark List View
class BookmarkListView(APIView):
    """List all bookmarked posts for the authenticated user."""
    permission_classes = [IsAuthenticated]
    
    # List all bookmarked posts for the authenticated user
    def get(self, request):
        try:
            bookmarks = Bookmark.objects.filter(user=request.user).select_related('post')
            posts = [bookmark.post for bookmark in bookmarks]
            serializer = PostListSerializer(posts, many=True)
            success_message = {
                'success': True,
                'message': 'Bookmarked posts retrieved successfully.',
                'data': serializer.data
            }
            logger.info("Bookmarked posts retrieved successfully.")
            return Response(success_message, status=status.HTTP_200_OK)
        except Exception as e:
            exception_error_message = {
                'success': False,
                'message': f'An error occurred while retrieving bookmarked posts: {str(e)}',
                'data': None
            }
            logger.error(f"An error occurred while retrieving bookmarked posts: {str(e)}")
            return Response(exception_error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                                               
                                                                                              

