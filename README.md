# WHERE Waitlist Backend

A FastAPI backend for managing a waitlist system.

## Setup

1. Install dependencies:

   pip install -r requirements.txt

2. Set up environment variables in .env:

   ADMIN_KEY=your_secure_admin_key

3. Run the app:

   uvicorn main:app --reload

## Endpoints

- POST /waitlist: Add a new entry (JSON body with name, email, profession, meetupPlaces array, frequency, interests, reason)

- GET /waitlist: Get all entries (requires Bearer token with ADMIN_KEY in Authorization header)

## API Documentation

Once running, visit http://127.0.0.1:8000/docs for interactive API docs.