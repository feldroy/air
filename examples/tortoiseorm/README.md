# TortoiseORM Demo

This demo showcases how to integrate [Tortoise ORM](https://tortoise.github.io/) with [Air](https://github.com/feldroy/air), a modern Python web framework.

## Overview

The demo implements a simple tournament management system with the following entities:

- **Tournament**: Represents a competition (e.g., "Autumn Open", "Spring Invitational")
- **Event**: Specific events within a tournament (e.g., "Singles", "Doubles", "Team Relay")
- **Team**: Participating teams (e.g., "Red Rockets", "Blue Blazers", "Green Giants")

## Features

- Async database operations with Tortoise ORM
- PostgreSQL database integration
- Automatic database seeding with sample data
- Web interface displaying tournaments, events, and teams
- Migration support with Aerich

## Prerequisites

Python 3.14+, PostgreSQL, and the uv package manager.

## Setup

1. **Create the database:**
   ```bash
   createdb tortoisedemo
   ```

2. **Update database connection** (optional):
   Edit `config.py` and update the `TORTOISE_ORM` configuration with your PostgreSQL connection details:
   ```python
   "connections": {"default": "postgres://your_username@localhost:5432/tortoisedemo"}
   ```

3. **Install dependencies and run:**
   ```bash
   uv run tortoiseorm_demo.py
   ```

The application will automatically:
- Initialize the database schema
- Seed sample data (2 tournaments, 3 events, 3 teams)
- Start the web server

## Database Migrations (Optional)

For production use, you can set up proper migrations with Aerich:

1. **Initialize Aerich:**
   ```bash
   uvx --with asyncpg "aerich[toml]" init -t config.TORTOISE_ORM
   ```

2. **Create initial migration:**
   ```bash
   uvx --with asyncpg "aerich[toml]" init-db
   ```

## Usage

Once running, visit `http://localhost:8000` to view the tournament data. The page displays:

- All tournaments
- Events within each tournament
- Teams participating in each event

## Project Structure

- `tortoiseorm_demo.py`: Main application file with Air routes and Tortoise setup
- `models.py`: Tortoise ORM model definitions
- `config.py`: Database configuration
- `pyproject.toml`: Aerich migration configuration

## Dependencies

- `air[standard]`: Web framework
- `asyncpg`: PostgreSQL driver for async operations
- `tortoise-orm[asyncpg]`: Tortoise ORM with PostgreSQL support</content>
