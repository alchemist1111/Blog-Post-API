from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

# Timestamps model
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

# Category model
class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'categories'
        
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Tag model
class Tag(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    
    class Meta:
        db_table = 'tags'
        
        ordering = ["name"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name   


# Post model
class Post(TimeStampedModel):
    class PostStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'  
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="posts/featured/", blank=True, null=True)           
    status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)  # Track post views
    published_at = models.DateTimeField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)
    
    class Meta:
        db_table = 'posts'
        
        ordering = ["-published_at", "-created_at"]
        
        indexes = [
            models.Index(fields=["status", "-published_at"], name='idx_post_status_published_at'),
            models.Index(fields=["category", "status"], name='idx_post_category_status'),
            models.Index(fields=["author", "status"], name='idx_post_author_status'),
            models.Index(fields=["is_featured", "status"], name='idx_post_featured_status'),
            models.Index(fields=["views_count"], name='idx_post_views_count'),
        ]
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists(): # Exclude the current instance when checking for existing slugs
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title 

# Post image model
class PostImage(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="posts/images/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)  # For ordering images within a post
    
    class Meta:
        db_table = 'post_images'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=["post", "order"], name='idx_post_image_order'),
        ]
    
    def __str__(self):
        return f"Image {self.order} for {self.post.title}"    

class Comment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies') # Self-referential foreign key for nested comments
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'comments'
        
        ordering = ["created_at"]
        
        indexes = [
            models.Index(fields=["post", "is_approved"], name='idx_post_approved_comments'),  # For efficient retrieval of approved comments for a post
            models.Index(fields=["author"], name='idx_comment_author'),  # For efficient retrieval of comments by a specific user
            models.Index(fields=["parent"], name='idx_comment_parent'),  # For efficient reply queries
        ] 
    
    def __str__(self):
        return f"Comment by {self.author.full_name} on {self.post.title}"

# Like model
class Like(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes') # User who liked the post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes') # Post that was liked
    
    class Meta:
        db_table = 'likes'
        ordering = ["-created_at"]
        
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')  # Prevent duplicate likes
        ]
        
        indexes = [
            models.Index(fields=["user", "post"], name='idx_user_post_like'),  # For efficient like lookups
        ] 
        
    def __str__(self):
        return f"{self.user.full_name} liked {self.post.title}"   

# Bookmark model
class Bookmark(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks') # User who bookmarked the post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks') # Post that was bookmarked
    
    class Meta:
        db_table = 'bookmarks'
        ordering = ["-created_at"]
        
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_bookmark')  # Prevent duplicate bookmarks
        ]
        
        indexes = [
            models.Index(fields=["user", "post"], name='idx_user_post_bookmark'),  # For efficient bookmark lookups
        ]  
    
    def __str__(self):
        return f"{self.user.full_name} bookmarked {self.post.title}"            
    
