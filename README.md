# Django E-Commerce Store

## Overview

This is a full-featured e-commerce application built using Python and Django. The store includes user authentication, product browsing, cart management, order processing, and email notifications. The application keeps a record of all previous orders, allowing users to track their purchase history.

## Features

- **User Authentication:** Secure sign-up and login forms.
- **Product Management:** Browse, search, and view product details.
- **Cart Management:** Add, remove, and update items in the shopping cart.
- **Order Processing:** Place orders and receive email notifications.
- **Order History:** View previous orders and their details.
- **Email Handling:** Send order confirmation and status updates via email.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/django-ecommerce-store.git
    cd django-ecommerce-store
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for accessing the Django admin panel:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://127.0.0.1:8000/`.

## Configuration

To configure email handling, add your email settings to the `settings.py` file:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
