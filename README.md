# Food Delivery System

A full-stack food ordering and delivery system built with Django REST Framework and React.

## Features

- User authentication and authorization
- Restaurant listing and management
- Menu management
- Order processing
- Real-time order tracking
- Payment integration
- Delivery management

## Tech Stack

### Backend
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication

### Frontend
- React
- Redux
- Material-UI
- Axios

## Setup Instructions

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Documentation

The API documentation will be available at `/api/docs/` when the server is running.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 