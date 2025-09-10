# ICT_U-Event-booking-website-with-react-and-django

Event Booking API Backend
This is the Django backend for an event booking system, designed to handle user registration, authentication, event creation, and booking management. It integrates with a React frontend and supports image uploads for events.
Prerequisites

Python 3.8+
Django 5.0.6
PostgreSQL (optional, SQLite is used by default)

Setup Instructions

Clone the Repository:
git clone <https://github.com/chewi-clinton/ICT_U-Event-booking-website-with-react-and-django/>
cd event_booking


Install Dependencies:
pip install -r requirements.txt


Configure Settings:

Update event_booking/settings.py with your SECRET_KEY and database settings if using PostgreSQL.
Ensure MEDIA_ROOT and MEDIA_URL are set for image uploads.


Apply Migrations:
python manage.py makemigrations
python manage.py migrate


Run the Server:
python manage.py runserver

The API will be available at http://localhost:8000/api/.


Key Features

User Management: Register and authenticate users via token-based authentication.
Event Management: Admins can create events with images; users can view and book events.
Attendee Auto-Creation: Attendees are automatically created from user data during registration or booking.
Admin Interface: Manage events, bookings, speakers, and sessions (attendee creation is disabled in admin).

API Endpoints

POST /api/register/: Register a new user.

POST /api/login/: Obtain an authentication token.

GET /api/events/: List all events.

POST /api/book/: Book seats for an event (authenticated users only).

POST /api/events/create/: Create a new event (admin only).

Requirements
See requirements.txt for dependencies:

Django==5.0.6
djangorestframework==3.15.1
Pillow==10.3.0
django-cors-headers==4.3.1

Notes

Configure CORS_ALLOWED_ORIGINS in settings.py to allow requests from the React frontend (e.g., http://localhost:3000).
Ensure Pillow is installed for image handling.
For production, use a WSGI server like gunicorn and a production database.

