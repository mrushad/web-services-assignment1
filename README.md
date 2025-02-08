# Web Services and Cloud-Based Systems

(Assignment 1 - Group 13)

This project implements an URL shortening service using RESTful API. The service allows users to generate a short ID for URLs, retrieve the original URLs using the short ID, update and delete the URLs.

## Features

- **Generate short ID**: Generate an unique identifier for URL.
- **Retrieve URL**: Retrieve original URL using short ID.
- **List URL**: List all stored short IDs.
- **Update URL**: Update URL for a given short ID.
- **Delete URL**: Delete a specific URL using its short ID.
- **Clear Database**: Clear all stored URLs.

## Prerequisites

- Python 3.13.1 or higher
- Flask
- requests module (for testing)

## Setup Instructions

Clone the repository to your local machine:

```jsx
git clone <repository-url>
cd web-services-assignment1
```

Navigate to backend folder:

```jsx
cd backend
```

Set the FLASK_APP environment variable and run the Flask application:

```jsx
export FLASK_APP=./api/index.py
flask run -h 0.0.0.0
```

The API will be accessible at `http://127.0.0.1:5000`

## Running Tests

Navigate to test folder:

```jsx
cd backend/test
```

Run test file:

```jsx
python3 -s test.py
```
