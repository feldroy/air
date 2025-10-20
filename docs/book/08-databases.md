# Working with Databases

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

Air is database-agnostic and works with any Python database library. Here's how to integrate common database solutions:

## Using SQLAlchemy

Let's add database functionality to our blog:

```bash
uv add sqlalchemy "psycopg2-binary"
```

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database setup
DATABASE_URL = "postgresql://postgres:password@localhost:5432/myblog"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Now you can use database models in your routes
@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return {"users": [{"id": u.id, "username": u.username} for u in users]}
```

## Using Tortoise ORM

Alternatively, you can use async ORMs like Tortoise ORM:

```bash
uv add "tortoise-orm[asyncpg]"
```

```python
from tortoise.models import Model
from tortoise import fields
from tortoise import Tortoise


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name='posts')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


# Initialize database
async def init_db():
    await Tortoise.init(
        db_url='sqlite://myblog.db',
        modules={'models': ['__main__']}  # Use your actual module path
    )
    await Tortoise.generate_schemas()
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add database integration with SQLAlchemy and Tortoise ORM"
```