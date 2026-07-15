# COLDSOLT Dancing - Agent Instructions

## Project Overview
This is a Django web application for booking dance lessons at a dancing school.
Built with Django 6.x and HTMX for dynamic UI updates.

## Tech Stack
- Python 3.14
- Django 6.x
- HTMX
- SQLite

## Project Structure
- `booking/` - Main Django app (models, views, templates)
- `coldsolt/` - Django project settings
- `manage.py` - Django management commands

## Running the Project
```bash
uv run python manage.py runserver
```

## Code Style
- Use Ruff for formatting and linting
- Follow Django conventions for models, views, and templates

## Key Models
- `Instructor` - Dance instructors (up to 5)
- `User` - Registered users
- `Reservation` - Bookings (date, slot 1-3, instructor, user)

## Database Schema

### Instructor
- id (auto)
- name: CharField(max_length=100)

### User
- id (auto)
- name: CharField(max_length=100)
- password: CharField(max_length=100)

### Reservation
- id (auto)
- date: DateField
- slot: IntegerField (1=Morning, 2=Afternoon, 3=Evening)
- instructor: ForeignKey(Instructor)
- user: ForeignKey(User)

## Testing
Run tests with:
```bash
uv run python manage.py test
```