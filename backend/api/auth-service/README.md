# Web Services and Cloud-Based Systems

(Assignment 2 - Group 13)

(Need to update description)

## Prerequisites

- Python 3.13.1 or higher
- Flask
- requests module (for testing)
- Redis

## Setup Instructions

Navigate to backend folder:

```jsx
cd web-services-assignment1/backend
```

Start redis server at port 6380:

```jsx
redis-server --port 6380
```

Activate the virtual environment:

```jsx
source venv/bin/activate
```

Set the FLASK_APP environment variable and run the Flask application:

```jsx
export FLASK_APP=./api/auth-service/auth_service.py
flask run -h 0.0.0.0
```

The API will be accessible at `http://127.0.0.1:5001`
