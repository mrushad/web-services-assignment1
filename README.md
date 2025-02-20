# Web Services and Cloud-Based Systems

(Assignment 2 - Group 13)

In extension to the URL shortening service in assignment 1, this includes an authentication service to manage user accounts and secure access to the URL shortening service.

## Features

- **Generate short ID**: Generate an unique identifier for URL.
- **Retrieve URL**: Retrieve original URL using short ID.
- **List URL**: List all stored short IDs.
- **Update URL**: Update URL for a given short ID.
- **Delete URL**: Delete a specific URL using its short ID.
- **Clear Database**: Clear all stored URLs.

### Authentication Service
- **Create User**: Register a new user account.
- **Update Password**: Change the password for an existing user.
- **Login**: Authenticate a user and generate a JWT token.
- **Logout**: Revoke a user's JWT token.
- **Verify Token**: Verify the validity of a JWT token.

## Prerequisites

- Python 3.13.1 or higher
- Flask
- Redis
- requests module (for testing)

## Setup Instructions

Navigate to backend folder:

```jsx
cd web-services-assignment1/backend
```

Install redis and start a redis service. The last command should return `PONG` to show the redis server is running successfully:

```jsx
brew install redis
brew services start redis
redis-cli ping
```

To start the URL shortening service, set the FLASK_APP environment variable and run the Flask application:

```jsx
export FLASK_APP=./api/url-shortener-service/index.py
flask run -h 0.0.0.0
```

The API will be accessible at `http://127.0.0.1:5000`

To start the authentication service, in a different terminal, set the FLASK_APP environment variable and run the Flask application:

```jsx
export FLASK_APP=./api/auth-service/auth_service.py
flask run --port=5001
```

The API will be accessible at `http://127.0.0.1:5001`



## Running Tests

From backend directory, activate the virtual environment:

```jsx
source venv/bin/activate
```

Navigate to test folder:

```jsx
cd api/test
```

Run test file:

```jsx
python3 -s test_app.py
```
