# Restaurant Booking System

## Overview
A modern restaurant booking system built with Django, featuring modular architecture, JWT authentication, and comprehensive API documentation.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.x

### Environment Setup
1. Clone the repository
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Configure the environment variables in `.env`

### Running with Docker
1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
2. The application will be available at `http://127.0.0.1/:8000`
3. Initial superuser credentials:
   - Email: admin@admin.com
   - Password: @123

### Local Development Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Architecture

### Modular Design
The project follows a clean, modular architecture with clear separation of concerns:

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
|    User     | --> |  API Layer  | --> |  Services   |
|  Interface  |     |  (Views)    |     |  Layer      |
|             |     |             |     |             |
+-------------+     +-------------+     +-------------+
                                              |
                                              v
                                       +-------------+
                                       |             |
                                       | Repository  |
                                       |   Layer     |
                                       |             |
                                       +-------------+
```

### Core Components

1. **Repository Layer**
   - Abstracts database operations
   - Implements data access patterns
   - Ensures clean separation from business logic

2. **Service Layer**
   - Contains core business logic
   - Implements booking rules and table allocation
   - Handles price calculations and validations

3. **API Layer**
   - RESTful endpoints using Django REST Framework
   - JWT-based authentication
   - Swagger UI integration for API documentation

### Authentication
- Stateless JWT (JSON Web Token) authentication
- Token-based authorization for API endpoints
- Custom user model with email authentication

## Features
- Table management (10 tables with 4-10 seats)
- Smart table allocation algorithm
- Pricing rules based on seat count
- Booking creation and management
- User authentication and authorization
- API documentation with Swagger UI
