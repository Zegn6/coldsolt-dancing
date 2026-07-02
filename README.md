# COLDSOLT Dancing

A web application for booking dance lessons at a dancing school.
Built for the Web Engineering course at the University of Aizu.

## Project Overview

Users can select an instructor, pick an available date and time slot,
and confirm a booking. The calendar updates dynamically using HTMX
without reloading the page.

## Tech Stack

- Python 3.14
- Django 6.x
- HTMX

## Tools

- **uv**: package manager
- **Ruff**: code formatting and linting
- **Coverage**: test coverage measurement

## Setup

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```