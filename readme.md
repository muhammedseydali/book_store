# Library Management System API

An API application built with Django Rest Framework for managing a Library Management System.

## Functionality

The Library Management System API provides the following functionalities:

- User Management:
  - Custom user model with proper authentication and authorization.
- Book Management:
  - Storing book details, including title, author, year of publication, and more.
  - Tracking the number of available books.
- Borrow/Return Tracking:
  - Tracking book borrow and return status by users.
  - Recording due dates for borrowed books.
- Additional Tables (if necessary):
  - You can extend the database schema with additional tables as needed.
- Pagination and Filtering:
  - API endpoints to list book details with pagination.
  - Filtering and searching based on book name, author, year of publication, and date range for borrow and return.
  - Ordering based on book name and year of publication with pagination.
- Email Notifications:
  - Sending email notifications for borrow and return confirmations.

## Project Details

- Database: SQLite (default database in Django)

## Setup

To run this project locally, follow these steps:

### Prerequisites

asgiref==3.7.2
Django==4.2.5
django-filter==23.3
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
PyJWT==2.8.0
pytz==2023.3.post1
sqlparse==0.4.4
typing_extensions==4.8.0
tzdata==2023.3


### Installation

1. Clone this repository:
2. Create virtual environment using python 3 or above
3. Cd to project/
4. pip install -r requirements.txt
5. python manage.py runserver


# swagger implimentation

### follow this link
http://127.0.0.1:8000/swagger/