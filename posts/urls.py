from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    TagListView,
    TagDetailView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostImageCreateView,
    PostImageDeleteView,
    CommentListCreateView,
    CommentDeleteView,
    LikeToggleView,
    BookmarkToggleView,
    BookmarkListView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    # Tags
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag-detail'),

    # Posts
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Post images
    path('<slug:slug>/images/', PostImageCreateView.as_view(), name='post-image-create'),
    path('<slug:slug>/images/<uuid:image_id>/', PostImageDeleteView.as_view(), name='post-image-delete'),

    # Comments
    path('<slug:slug>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<slug:slug>/comments/<uuid:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),

    # Likes
    path('<slug:slug>/like/', LikeToggleView.as_view(), name='post-like-toggle'),

    # Bookmarks
    path('<slug:slug>/bookmark/', BookmarkToggleView.as_view(), name='post-bookmark-toggle'),
    path('bookmarks/me/', BookmarkListView.as_view(), name='post-bookmark-list'),
]