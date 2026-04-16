import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    # Filter by title (case-insensitive partial match)
    title = django_filters.CharFilter(lookup_expr='icontains')

    # Filter by content (case-insensitive partial match)
    content = django_filters.CharFilter(lookup_expr='icontains')

    # Filter by status
    status = django_filters.ChoiceFilter(choices=Post.PostStatus.choices)

    # Filter by category
    category = django_filters.UUIDFilter(field_name='category__id')

    # Filter by category slug
    category_slug = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')

    # Filter by tag
    tags = django_filters.UUIDFilter(field_name='tags__id')

    # Filter by tag slug
    tag_slug = django_filters.CharFilter(field_name='tags__slug', lookup_expr='exact')

    # Filter by author
    author = django_filters.UUIDFilter(field_name='author__id')

    # Filter by is_featured
    is_featured = django_filters.BooleanFilter()

    # Filter by published_at range
    published_after = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'status', 'category', 'category_slug',
            'tags', 'tag_slug', 'author', 'is_featured',
            'published_after', 'published_before',
        ]