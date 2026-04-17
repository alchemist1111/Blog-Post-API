from rest_framework import serializers
from .models import Post, PostImage, Category, Tag, Comment, Like, Bookmark


# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


# Tag serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


# Post image serializer
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'caption', 'order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'author_name', 'body', 'parent',
            'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author_name', 'created_at', 'updated_at']

    def get_replies(self, obj):
        """Return direct replies to this comment."""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


# Like serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']


# Bookmark serializer
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']


# Post list serializer — lightweight for list views
class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author_name', 'category_name', 'tags', 'title', 'slug',
            'excerpt', 'featured_image', 'status', 'is_featured',
            'published_at', 'views_count', 'likes_count', 'comments_count',
            'bookmarks_count', 'reading_time', 'created_at', 'updated_at',
        ]
        read_only_fields = fields

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    def get_reading_time(self, obj):
        """Estimate reading time based on average 200 words per minute."""
        word_count = len(obj.content.split())
        minutes = max(1, round(word_count / 200))
        return f"{minutes} min read"


# Post detail serializer — full detail for single post view
class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author_name', 'category', 'tags', 'title', 'slug',
            'excerpt', 'content', 'featured_image', 'images', 'status',
            'is_featured', 'published_at', 'views_count', 'likes_count',
            'comments_count', 'bookmarks_count', 'reading_time',
            'meta_title', 'meta_description', 'created_at', 'updated_at',
            'comments',
        ]
        read_only_fields = [
            'id', 'author_name', 'slug', 'views_count', 'published_at',
            'created_at', 'updated_at',
        ]

    def get_comments(self, obj):
        """Return only top-level comments. Replies are nested inside each comment."""
        top_level_comments = obj.comments.filter(parent__isnull=True)
        return CommentSerializer(top_level_comments, many=True).data

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    def get_reading_time(self, obj):
        """Estimate reading time based on average 200 words per minute."""
        word_count = len(obj.content.split())
        minutes = max(1, round(word_count / 200))
        return f"{minutes} min read"


# Post create/update serializer
class PostWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Post
        fields = [
            'category', 'tags', 'title', 'excerpt', 'content',
            'featured_image', 'status', 'is_featured',
            'meta_title', 'meta_description',
        ]

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("Title cannot exceed 255 characters.")
        return value

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Post.PostStatus.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Choose from: {valid_statuses}")
        return value

    def validate(self, data):
        """Set published_at when status changes to published."""
        from django.utils import timezone
        if data.get('status') == Post.PostStatus.PUBLISHED:
            if self.instance is None or self.instance.status != Post.PostStatus.PUBLISHED:
                data['published_at'] = timezone.now()
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance