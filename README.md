# Django Authenticator

## Project Overview

This is a web-based user authentication system built with Django. The application allows users to register accounts, verify their email addresses, log in, and log out. It demonstrates secure user management practices including email-based account activation and session handling.

## Features

- User registration with input validation (username length, alphanumeric check, email uniqueness)
- Password confirmation during registration
- Email verification for account activation
- Secure login and logout functionality
- Custom token-based activation system
- User session management
- Responsive web interface

## Tech Stack

- **Language**: Python
- **Framework**: Django 5.1
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Email Service**: SMTP (Gmail)

## Project Architecture / Workflow

The application follows Django's Model-View-Template (MTV) pattern:

1. **Models**: Uses Django's built-in User model for storing user accounts
2. **Views**: Handle HTTP requests for registration, login, logout, and account activation
3. **Templates**: Render HTML pages for user interaction
4. **URLs**: Route requests to appropriate view functions

**User Registration Flow**:
- User submits registration form
- Server validates input and creates inactive user account
- Welcome email and activation email are sent
- User clicks activation link to verify email and activate account

**Login Flow**:
- User submits credentials
- Server authenticates and creates session
- User is redirected to authenticated home page

## Setup & Installation

### Prerequisites
- Python 3.x
- Django 5.1
- Virtual environment (recommended)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Authenticator
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install django
   ```

4. Configure email settings in `LoginSystem/info.py`:
   - Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` with your Gmail credentials
   - Note: For production, use environment variables instead

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## Usage

1. **Home Page**: Displays welcome message and login/register options
2. **Registration**: Fill out the registration form with username, name, email, and password
3. **Email Verification**: Check email for activation link and click to activate account
4. **Login**: Use username and password to log in
5. **Logout**: Click logout button to end session

## Key Learnings / Concepts Demonstrated

- Django project structure and configuration
- User authentication and session management
- Email integration with Django
- Custom token generation for secure links
- Form validation and error handling
- URL routing and view functions
- Template rendering with context variables
- Static file management
- Database migrations and models

## Future Improvements

- Implement password reset functionality
- Add user profile management
- Enhance security with two-factor authentication
- Migrate to PostgreSQL for production deployment
- Add comprehensive test coverage