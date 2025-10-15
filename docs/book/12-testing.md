# Testing

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

## Unit Testing

Air applications can be tested using FastAPI's test client. Here's a comprehensive testing approach for all aspects of your application:

```python
import pytest
from fastapi.testclient import TestClient
from main import app, get_articles, get_article

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "My Personal Blog" in response.text
    assert "Latest Articles" in response.text

def test_article_list():
    response = client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert isinstance(data["articles"], list)

def test_article_detail():
    # Test with a known article slug (assuming you have hello-world.md)
    response = client.get("/hello-world")
    assert response.status_code == 200
    assert "Hello World" in response.text

def test_contact_form():
    response = client.post("/contact", data={
        "name": "Test User",
        "email": "test@example.com",
        "message": "Hello, world!",
        "subject": "Test Subject"
    })
    assert response.status_code == 200
    assert "Thank You!" in response.text

def test_contact_form_invalid():
    # Test form with missing required fields
    response = client.post("/contact", data={
        "name": "",  # Missing required name
        "email": "invalid-email",  # Invalid email
        "message": "Short"  # Too short
    })
    assert response.status_code == 200
    assert "Please correct the errors below:" in response.text

def test_api_article_detail():
    response = client.get("/api/articles/hello-world")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "slug" in data
    assert data["slug"] == "hello-world"

def test_api_article_not_found():
    response = client.get("/api/articles/nonexistent-slug")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data

def test_htmx_endpoints():
    # Test HTMX counter functionality
    # Reset counter first
    response = client.post("/api/reset")
    assert response.status_code == 200
    
    # Test increment
    response = client.post("/api/increment")
    assert response.status_code == 200
    assert "1" in response.text
    
    # Test decrement
    response = client.post("/api/decrement")
    assert response.status_code == 200
    assert "0" in response.text
```

## Testing with HTMX

Test HTMX endpoints with proper headers and state management:

```python
def test_htmx_increment():
    """Test HTMX increment functionality."""
    # Reset counter to known state
    reset_response = client.post("/api/reset")
    assert reset_response.status_code == 200
    assert "0" in reset_response.text
    
    # Test increment
    response = client.post("/api/increment")
    assert response.status_code == 200
    assert "1" in response.text

def test_htmx_headers():
    """Test HTMX-specific headers are handled properly."""
    response = client.post("/api/increment", headers={
        "HX-Request": "true",  # HTMX makes this header
        "HX-Target": "counter"
    })
    assert response.status_code == 200
    assert "1" in response.text

def test_htmx_search():
    """Test HTMX search functionality."""
    response = client.post("/api/search", data={"q": "hello"})
    assert response.status_code == 200
    assert "search-results" in response.text

def test_htmx_search_empty():
    """Test HTMX search with empty query."""
    response = client.post("/api/search", data={"q": ""})
    assert response.status_code == 200
    assert "Enter a search term" in response.text
```

## Database Testing

If using a database, implement proper testing strategies:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

def test_database_operations():
    """Test database operations."""
    # This would test actual database operations if you had them
    response = client.get("/users")
    assert response.status_code == 200
```

## Form Validation Testing

Test your Air Forms validation thoroughly:

```python
def test_contact_form_validation_valid():
    """Test ContactForm with valid data."""
    response = client.post("/contact", data={
        "name": "Valid Name",
        "email": "valid@example.com",
        "subject": "Valid Subject",
        "message": "This is a valid message with sufficient length."
    })
    assert response.status_code == 200
    assert "Thank You!" in response.text

def test_contact_form_validation_invalid():
    """Test ContactForm with invalid data."""
    response = client.post("/contact", data={
        "name": "A",  # Too short
        "email": "invalid-email",  # Invalid email
        "subject": "Hi",  # Too short
        "message": "Hi"  # Too short
    })
    assert response.status_code == 200
    assert "Please correct the errors below:" in response.text
    # Check that errors are displayed
    assert "name" in response.text
    assert "email" in response.text

def test_contact_form_missing_required():
    """Test ContactForm with missing required fields."""
    response = client.post("/contact", data={})
    assert response.status_code == 200
    assert "Please correct the errors below:" in response.text
```

## API Testing

Comprehensive API endpoint testing:

```python
def test_api_articles_response_structure():
    """Test that API response has correct structure."""
    response = client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    
    assert "articles" in data
    assert "total" in data
    assert isinstance(data["total"], int)
    
    if data["articles"]:  # If there are articles
        article = data["articles"][0]
        assert "id" in article
        assert "title" in article
        assert "slug" in article
        assert "description" in article
        assert "date" in article
        assert "author" in article
        assert "tags" in article
        assert "url" in article

def test_api_article_detail_response_structure():
    """Test that API article detail response has correct structure."""
    response = client.get("/api/articles/hello-world")
    if response.status_code == 200:  # Only if article exists
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "slug" in data
        assert "description" in data
        assert "date" in data
        assert "author" in data
        assert "tags" in data
        assert "content" in data
        assert "html_content" in data

def test_api_404_handling():
    """Test API 404 error handling."""
    response = client.get("/api/articles/nonexistent-article")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "Article not found"
```

## Error Handling Testing

Test your error handlers:

```python
def test_404_error_page():
    """Test 404 error page."""
    response = client.get("/nonexistent-page")
    assert response.status_code == 404
    assert "Page Not Found" in response.text

def test_500_error_page():
    """Test 500 error page (requires triggering an actual server error)."""
    # This would require creating a route that raises an exception
    pass
```

## Integration Testing

Test the complete user journey:

```python
def test_complete_user_flow():
    """Test a complete user journey."""
    # 1. Visit homepage
    response = client.get("/")
    assert response.status_code == 200
    assert "My Personal Blog" in response.text
    
    # 2. View articles list
    response = client.get("/")
    assert "Latest Articles" in response.text
    
    # 3. Submit contact form
    response = client.post("/contact", data={
        "name": "Integration Test User",
        "email": "integration@test.com",
        "subject": "Integration Test",
        "message": "This is a test message during integration testing."
    })
    assert response.status_code == 200
    assert "Thank You!" in response.text
    
    # 4. Verify API access
    response = client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
```

## Testing Best Practices

1. **Use fixtures for common setup:**

```python
@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

@pytest.fixture
def sample_article():
    """Provide sample article data for tests."""
    return {
        "title": "Test Article",
        "slug": "test-article",
        "description": "A test article",
        "content": "# Test Article\\n\\nThis is a test article."
    }
```

2. **Test different data scenarios:**

   - Valid data
   - Invalid data
   - Boundary conditions
   - Edge cases

3. **Use parameterized tests for multiple scenarios:**
```python
@pytest.mark.parametrize("name,email,message,expected_status", [
    ("Valid User", "valid@example.com", "Valid message", 200),
    ("", "valid@example.com", "Valid message", 200),  # Should fail validation
    ("Valid User", "invalid-email", "Valid message", 200),  # Should fail validation
])
def test_contact_form_scenarios(name, email, message, expected_status):
    response = client.post("/contact", data={
        "name": name,
        "email": email,
        "message": message
    })
    assert response.status_code == expected_status
```

4. **Mock external dependencies:**
```python
from unittest.mock import patch

def test_external_api_call():
    """Test functionality that calls external APIs."""
    with patch('main.external_api_call') as mock_api:
        mock_api.return_value = {"status": "success"}
        response = client.get("/external-call")
        assert response.status_code == 200
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add comprehensive testing framework"
```