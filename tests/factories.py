import factory
from factory.django import DjangoModelFactory

# This file defines factory classes for creating test instances of models.
class UserFactory(DjangoModelFactory):
    """Factory for creating User instances."""
    class Meta:
        model = 'accounts.User'
        
    full_name = factory.Sequence(lambda n: f'Test User {n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.full_name.lower().replace(" ", "")}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'TestPassword@123')
    password_confirmation = factory.PostGenerationMethodCall('set_password', 'TestPassword@123')

# Factory for Category model
class CategoryFactory(DjangoModelFactory):
    """Factory for creating Category instances."""
    class Meta:
        model = 'posts.Category'
    
    name = factory.Sequence(lambda n: f'Category {n}')
    slug = factory.Sequence(lambda n: f'category-{n}')
    description = factory.Faker('paragraph')           