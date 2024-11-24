# Library Service

A Django-based web application for managing library borrowing, books, and users. The project supports integration with Stripe for payments, Telegram notifications, and has a robust test suite for reliable operations. The application is containerized using Docker for easy deployment.

## Features

	•	User Management: Supports user authentication and admin control.
	•	Book Inventory: Manage books, including titles, authors, pricing, and inventory.
	•	Borrowing System:
	•	Borrow books with expected return dates.
	•	Mark borrowed books as returned.
	•	Integration with Stripe for payment processing.
	•	Notifications:
	•	Telegram notifications for borrowing and payment status updates.
	•	API Documentation:
	•	Auto-generated API documentation using DRF Spectacular.
	•	Background Tasks:
	•	Celery tasks for async operations with Redis as the message broker.
	•	Test Suite:
	•	Comprehensive tests for models, views, and serializers with 87% coverage.

## Tech Stack

	•	Backend: Django, Django REST Framework (DRF)
	•	Database: PostgreSQL
	•	Messaging: Redis, Celery
	•	Payments: Stripe
	•	Notifications: Telegram Bot
	•	Containerization: Docker & Docker Compose
	•	Task Scheduling: Django-Celery-Beat

## Installation

### 1. Clone the repository

```
git clone https://github.com/AndriZhok/Library-Service-Project.git
```


### 2. Set up environment variables

Create a .env file in the root directory with the following variables:

```
TELEGRAM_URL=https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/sendMessage
TELEGRAM_CHAT_ID=<YOUR_TELEGRAM_CHAT_ID>
STRIPE_API_KEY=<YOUR_STRIPE_SECRET_KEY>
SECRET_KEY=<YOUR_DJANGO_SECRET_KEY>
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=library_service
POSTGRES_HOST=db
POSTGRES_PORT=5432
DEBUG=True
```

### 3. Build and run the Docker containers

Ensure Docker is installed and running, then execute:

```
docker-compose up --build
```

This will start:
	•	Web: Django app
	•	Database: PostgreSQL
	•	Message Broker: Redis

### 4. Apply migrations and create superuser

Open a terminal in the running container:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Access the application

	•	Visit: http://localhost:8000
	•	API Docs: http://localhost:8000/api/schema/swagger-ui/

## Testing

Run all tests with coverage:

```
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

## Usage

### 1. Add Books

Admins can add books to the inventory through the admin panel or API.

### 2. Borrow Books

	•	Users can borrow books and make payments through Stripe.
	•	Notifications are sent via Telegram.

### 3. Return Books

Mark borrowed books as returned to update inventory.

### 4. Monitor Background Tasks

Celery processes asynchronous tasks for notifications and payment processing.

API Endpoints

Key endpoints:

	•	Books: /api/books/
	•	Borrowing: /api/borrowings/
	•	Payments: /api/payments/

### For detailed API documentation, visit: Swagger UI

Development

Linting

Ensure code quality with flake8:

docker-compose exec web flake8

Add a new dependency

Update the requirements.txt and rebuild the Docker container:

docker-compose build

### Contributing

	1.	Fork the repository.
	2.	Create a new branch for your feature or bugfix.
	3.	Commit your changes.
	4.	Submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

	•	Django
	•	Stripe
	•	Docker
	•	Redis
	•	Telegram Bot API
