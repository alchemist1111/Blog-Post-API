# Blog Post Platform API

A powerful Django REST Framework-based API for managing a blog post platform with support for posts, categories, tags, comments, likes, and bookmarks.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Framework | Django 6.0.3 |
| API | Django REST Framework 3.17.1 |
| Database | SQLite (development) / PostgreSQL 18 (production) |
| Caching | Redis 7 |
| Image Processing | Pillow 12.1.1 |
| Testing | Pytest 9.0.3, Factory Boy 3.3.3 |
| Task Queue | Optional Celery integration |
| Web Server | Gunicorn (production) |

---

## Features

### Core Functionality
- **Blog Post Management** — Create, read, update, and delete blog posts
- **Post Status Management** — Draft, Published, and Archived statuses with automated slug generation
- **Search and Filtering** — Filter posts by title, category, tags, author, and status
- **Pagination** — Automatic pagination with configurable page size (default: 10 items per page)
- **Rich Content Support** — Posts include title, excerpt, content, featured image, and multiple post images

### User Management
- **Custom User Model** — Email-based authentication with UUID primary keys
- **User Registration** — Create new user accounts with email validation
- **User Profiles** — Extended profiles with bio, avatar, and social media links (Twitter, LinkedIn, GitHub)
- **Admin User Management** — Admin endpoints for managing users and permissions

### Content Organization
- **Categories** — Organize posts into categories with automatic slug generation
- **Tags** — Multiple tags per post for better discoverability
- **Post Images** — Multiple images per post with ordering and captions

### User Interactions
- **Comments** — Nested/threaded comments supporting replies
- **Likes** — Users can like posts (unique constraint prevents duplicate likes)
- **Bookmarks** — Users can bookmark posts for later reading

### Analytics & SEO
- **View Tracking** — Automatic post view count logging
- **Reading Time Estimation** — Calculated based on content word count (200 wpm)
- **Meta Tags** — Support for meta titles and descriptions
- **Featured Posts** — Highlight important posts

### Data Integrity
- **Automatic Timestamps** — `created_at` and `updated_at` on all models
- **Soft Deletes** — User soft delete with `deleted_at` field
- **Database Indexes** — Optimized queries on frequently filtered fields
- **Unique Constraints** — Prevent duplicate likes, bookmarks, emails, and slugs

---

## Project Structure

```
blog_post/
├── accounts/                 # User management app
│   ├── models.py            # User and UserProfile models
│   ├── serializers.py       # User serializers
│   ├── views.py             # User registration, login, profile management
│   ├── urls.py              # Account-related endpoints
│   ├── permissions.py       # Custom permissions
│   ├── validations.py       # Field validation logic
│   └── migrations/
├── posts/                    # Blog post app
│   ├── models.py            # Post, Category, Tag, Comment, Like, Bookmark models
│   ├── serializers.py       # DRF serializers for all models
│   ├── views.py             # CRUD endpoints
│   ├── urls.py              # Post-related endpoints
│   ├── permissions.py       # Custom permissions
│   ├── filters.py           # DjangoFilterBackend filter definitions
│   └── migrations/
├── blog_post/               # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tests/
│   ├── conftest.py
│   ├── factories.py
│   └── tests.py
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── db.sqlite3
```

---

## Installation

### Prerequisites
- Python 3.11+
- pip and virtualenv (or conda)
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "Blog Post"
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv blog
.\blog\Scripts\Activate
```

**macOS/Linux:**
```bash
python3 -m venv blog
source blog/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser

```bash
python manage.py createsuperuser
```

### Step 7: Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/accounts/register/` | Register a new user | No |
| POST | `/api/accounts/login/` | Login | No |
| GET | `/api/accounts/me/` | Get current user | Yes |
| PUT | `/api/accounts/me/update/` | Update current user | Yes |
| DELETE | `/api/accounts/me/delete/` | Soft delete account | Yes |
| GET | `/api/accounts/me/profile/` | Get user profile | Yes |
| PUT | `/api/accounts/me/profile/update/` | Update user profile | Yes |
| GET | `/api/accounts/admin/users/` | List all users | Admin |
| GET | `/api/accounts/admin/users/<id>/` | Get user details | Admin |

### Categories

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/posts/categories/` | List all categories | No |
| POST | `/posts/categories/` | Create category | Admin |
| GET | `/posts/categories/<slug>/` | Get category | No |
| PUT | `/posts/categories/<slug>/` | Update category | Admin |
| DELETE | `/posts/categories/<slug>/` | Delete category | Admin |

### Tags

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/posts/tags/` | List all tags | No |
| POST | `/posts/tags/` | Create tag | Admin |
| GET | `/posts/tags/<slug>/` | Get tag | No |
| PUT | `/posts/tags/<slug>/` | Update tag | Admin |
| DELETE | `/posts/tags/<slug>/` | Delete tag | Admin |

### Posts

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/posts/` | List posts (filtered & paginated) | No |
| POST | `/posts/create/` | Create a post | Yes |
| GET | `/posts/<slug>/` | Get post details | No |
| PUT | `/posts/<slug>/update/` | Update post | Author/Admin |
| DELETE | `/posts/<slug>/delete/` | Delete post | Author/Admin |
| POST | `/posts/<slug>/images/` | Add image to post | Author/Admin |
| DELETE | `/posts/<slug>/images/<id>/` | Delete post image | Author/Admin |

### Comments

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/posts/<slug>/comments/` | List post comments | No |
| POST | `/posts/<slug>/comments/` | Create comment | Yes |
| DELETE | `/posts/<slug>/comments/<id>/` | Delete comment | Author/Admin |

### Likes & Bookmarks

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/posts/<slug>/like/` | Like/unlike a post | Yes |
| POST | `/posts/<slug>/bookmark/` | Bookmark/unbookmark a post | Yes |
| GET | `/posts/bookmarks/me/` | List user's bookmarks | Yes |

### Filtering & Search

```
GET /posts/?search=Django&category=technology&status=published&is_featured=true
```

| Parameter | Description |
|-----------|-------------|
| `search` | Search in title, content, and excerpt |
| `category` | Filter by category slug |
| `tags` | Filter by tag slug |
| `author` | Filter by author ID or username |
| `status` | `draft`, `published`, or `archived` |
| `is_featured` | `true` or `false` |

---

## Response Format

All API responses follow a consistent structure:

```json
{
  "success": true,
  "message": "Description of response",
  "data": {}
}
```

---

## Docker Setup

```bash
# Build and start
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop
docker-compose down
```

- API: `http://localhost:8000/api/`
- Admin Panel: `http://localhost:8000/admin/`

---

## Configuration

### REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Authentication (Not Included — Setup Required)

> ⚠️ The project does not include built-in authentication. Configure JWT before using protected endpoints:

```bash
pip install djangorestframework-simplejwt
```

```python
INSTALLED_APPS = [..., 'rest_framework_simplejwt']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

---

## Testing

```bash
pytest            # Run all tests
pytest -v         # Verbose output
pytest --cov      # With coverage report
```

Test factories for generating test data are available in `tests/factories.py`.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| Migration errors | `python manage.py migrate --fake-initial` then `migrate` |
| Static files not loading | `python manage.py collectstatic --noinput` |
| Permission denied on venv (Linux/macOS) | `chmod +x blog/bin/activate` |

---

## Future Enhancements

- [ ] JWT / Token-based authentication
- [ ] Rate limiting on API endpoints
- [ ] Full-text search (PostgreSQL or Elasticsearch)
- [ ] Celery tasks for async operations
- [ ] WebSocket support for real-time updates
- [ ] API versioning
- [ ] Admin analytics dashboard
- [ ] Comment moderation workflow
- [ ] Post scheduling
- [ ] Swagger / OpenAPI documentation

---

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add your feature'`
3. Push: `git push origin feature/your-feature`
4. Open a pull request

---

## License

This project is licensed under the **MIT License** — see the `LICENSE` file for details.

---

## Project URL
project URL
```bash
      https://github.com/alchemist1111/Blog-Post-API.git
 ```