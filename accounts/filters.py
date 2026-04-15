import django_filters
from .models import User

class UserFilter(django_filters.FilterSet):
    # Filter by full name (case-insensitive partial match)
    full_name = django_filters.CharFilter(field_name='full_name', lookup_expr='icontains')
    
    # Filter by email (case-insensitive partial match)
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    
    # Filter by is_active
    is_active = django_filters.BooleanFilter(field_name='is_active')
    
    # Filter by is_staff
    is_staff = django_filters.BooleanFilter(field_name='is_staff')
    
    # Filter to include or exclude soft-deleted users
    is_deleted = django_filters.BooleanFilter(
        field_name='deleted_at',
        method='filter_is_deleted',
        label='Is Deleted'
    )
    
    # Filter by created_at date range
    def filter_is_deleted(self, queryset, name, value):
        """
            Filter users based on soft delete status.
            is_deleted=true  → only soft-deleted users
            is_deleted=false → only active (non-deleted) users
        """
        if value:
            return queryset.filter(deleted_at__isnull=False)
        return queryset.filter(deleted_at__isnull=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'is_active', 'is_staff', 'is_deleted']