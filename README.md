# Django Project

This is a basic Django project that includes two applications: `store` and `order`. Each app has its own views and is connected to the main project's URLs.

## Features

- Admin interface with superuser authentication.
- Two applications:
  - **Store**: Manages the store-related views.
  - **Order**: Manages the order-related views.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd myproject
2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
4. Apply the migrations:
   ```bash
   python manage.py migrate
5. Create a superuser for the admin panel:
   ```bash
   python manage.py createsuperuser
6. Run the development server:
   ```bash
   python manage.py runserver

## Applications
  # Store
    /store/: Displays the store home page.
    /store/products/: Displays the list of products.
    /store/categories/: Displays the list of categories.
  # Order
    /order/: Displays the order home page.
    /order/details/: Displays order details.
