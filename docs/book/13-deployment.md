# Deployment

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

## Production Deployment

Deploy your Air application just like any FastAPI application. For production environments, you'll want to use a production-ready ASGI server:

```bash
# Install production ASGI server
uv add "uvicorn[standard]" gunicorn

# For Unix systems (Linux/macOS)
uv add gunicorn uvicorn

# Run with gunicorn and uvicorn worker
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --keep-alive 5
```

For high-traffic applications, consider using Uvicorn directly or with a reverse proxy:

```bash
# Run Uvicorn directly (good for containerized environments)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Configuration for Production

Create a production-ready configuration:

```python title="config.py"
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/myblog")
    
    # Security settings
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    allowed_hosts: str = os.getenv("ALLOWED_HOSTS", "*")
    
    # CORS settings
    cors_allow_origins: str = os.getenv("CORS_ALLOW_ORIGINS", "")
    cors_allow_credentials: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    cors_allow_methods: str = os.getenv("CORS_ALLOW_METHODS", "*")
    cors_allow_headers: str = os.getenv("CORS_ALLOW_HEADERS", "*")
    
    # Application settings
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    admin_email: str = os.getenv("ADMIN_EMAIL", "admin@example.com")
    
    # Cache settings
    redis_url: Optional[str] = os.getenv("REDIS_URL")
    
    @property
    def cors_allow_origins_list(self) -> list:
        if self.cors_allow_origins:
            return [origin.strip() for origin in self.cors_allow_origins.split(",")]
        return ["*"]


settings = Settings()
```

## Docker Deployment

Create a production-ready `Dockerfile` with security and performance optimizations:

```dockerfile
# Use a non-root user for security
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /home/app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv sync --system

# Copy application code
COPY . .

# Change ownership to app user
RUN chown -R app:app /home/app

# Switch to app user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run with gunicorn
CMD ["/home/app/.venv/bin/gunicorn", "main:app", \
    "-w", "4", \
    "-k", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0:8000", \
    "--timeout", "120", \
    "--keep-alive", "5", \
    "--max-requests", "1000", \
    "--max-requests-jitter", "100"]
```

Create a `docker-compose.yml` for easy deployment:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myblog
      - SECRET_KEY=your-super-secret-key
      - DEBUG=False
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./articles:/home/app/articles  # For persistent article storage
    restart: unless-stopped

  db:
    image: postgres:18
    environment:
      - POSTGRES_DB=myblog
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl  # For SSL certificates
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

## Reverse Proxy Configuration

Create an Nginx configuration for production:

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream myblog {
        server web:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        
        client_max_body_size 100M;
        
        # Static files
        location /static {
            alias /home/app/static;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
        
        # API and application routes
        location / {
            proxy_pass http://myblog;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;
            
            # WebSocket support if needed
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

## Environment Configuration

Use environment variables for configuration. Create a `.env.example` file:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/dbname

# Security
SECRET_KEY=your-very-long-secret-key-here-make-it-random-and-secure

# Application
DEBUG=False
ADMIN_EMAIL=admin@yourdomain.com

# CORS
CORS_ALLOW_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Redis (for caching/session storage)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
```

## Production Settings

Create different settings for different environments:

```python title="config.py" (expanded)
import os
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Core settings
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/myblog")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY")
    allowed_hosts: str = os.getenv("ALLOWED_HOSTS", "*")
    
    # CORS
    cors_allow_origins: str = os.getenv("CORS_ALLOW_ORIGINS", "")
    cors_allow_credentials: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    cors_allow_methods: str = os.getenv("CORS_ALLOW_METHODS", "*")
    cors_allow_headers: str = os.getenv("CORS_ALLOW_HEADERS", "*")
    
    # Cache
    redis_url: Optional[str] = os.getenv("REDIS_URL")
    
    # Email (for contact forms, notifications)
    smtp_server: str = os.getenv("SMTP_SERVER", "localhost")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("SMTP_USERNAME")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")
    email_from: str = os.getenv("EMAIL_FROM", "noreply@yourdomain.com")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # File uploads
    max_upload_size: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    
    @property
    def cors_allow_origins_list(self) -> List[str]:
        if self.cors_allow_origins:
            return [origin.strip() for origin in self.cors_allow_origins.split(",")]
        return ["*"] if not self.debug else ["*"]

    @property
    def is_production(self) -> bool:
        return not self.debug
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

And update your main application to use these settings:

```python
# main.py (with production settings)
from config import settings
import air

# Initialize app with settings
app = air.Air(
    debug=settings.debug,
    title="My Personal Blog",
    version=settings.app_version
)

# Add CORS middleware if needed
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Scaling Considerations

For production applications, consider:

1. **Database Connection Pooling**: Use connection pools for database access
2. **Caching**: Implement caching with Redis or similar
3. **Static Files**: Serve static files through a CDN or reverse proxy
4. **Load Balancing**: Scale across multiple instances
5. **Monitoring**: Add logging and monitoring tools
6. **Health Checks**: Implement health check endpoints
7. **Security**: Use HTTPS, security headers, and authentication
8. **Backup Strategy**: Regular database and file backups
9. **Monitoring**: Application and infrastructure monitoring
10. **CDN**: Use a CDN for static assets

## Health Checks and Monitoring

Add health check endpoints:

```python
@app.get("/health")
def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "app": "My Personal Blog",
        "version": settings.app_version,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ready")
def readiness_check():
    """Readiness check to verify the app is ready to serve requests."""
    # Add checks for database, cache, etc.
    return {"status": "ready"}
```

## SSL/HTTPS Configuration

For production, always use HTTPS. You can handle this at the reverse proxy level (nginx) or with a service like Let's Encrypt:

```bash
# Using certbot for Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Performance Optimization

Optimize your production deployment:

```python
# In production settings, optimize for performance
if settings.is_production:
    # Add performance-related middleware
    from fastapi.middleware.gzip import GZipMiddleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Configure for production
    app.docs_url = "/docs" if settings.debug else None
    app.redoc_url = "/redoc" if settings.debug else None
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Complete deployment configuration"
```